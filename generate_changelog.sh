#! /bin/bash

# Declare a varaiable for caching
declare cache;

function id_current_tag() {
	local INPUT="${1}"
	git describe --tags --abbrev=0 ${INPUT}
}

function run_enumerate_tag_history() {
	local HEAD_TAG=$(id_current_tag HEAD)
	{ git rev-list --tags --ancestry-path "$(git tag --no-contains "${HEAD_TAG}" | sort -V | head -n1)^..HEAD" ; wait ;} | xargs -I{} git tag --points-at "{}" 2>/dev/null ;
	wait ;
}

function enumerate_tag_history() {
	if [[ -z "${cache}" ]] ; then
		cache=$(run_enumerate_tag_history | grep -vE "v?\d+.\d+.\d+-dev" ; wait;)
	fi ;
	printf "%s\n" "${cache}" ;
	wait ;
}

function id_parent_tag() {
	local INPUT="${1}"
	enumerate_tag_history | grep -A 1 -F -f <(id_current_tag ${INPUT} ) | tail -n1
	wait ;
}

# step 1: is designed to determine the current and previous Git tags and
# then construct a Git range based on these tags. If no argument is provided, it defaults to
# using the tags.
if [[ -z "${1}" ]] ; then
# GIT_CURRENT_TAG=$(id_current_tag)

for EACH_TAG in $(enumerate_tag_history | sort -Vr) ; do
GIT_PREVIOUS_TAG=$(id_parent_tag "${EACH_TAG}")
FALLBACK_GIT_RANGE="${EACH_TAG}...${GIT_PREVIOUS_TAG}"
"${0}" "${FALLBACK_GIT_RANGE}" || : ; wait ;
done;
exit 0 ;
fi ;
GIT_RANGE="${1:-${FALLBACK_GIT_RANGE}}"

# cache the git log
CHANGELOG_BUFFER=".chagelog_buffer.txt"
cat <(git log "${GIT_RANGE}" --reverse --pretty=format:"COMMIT_START%n%h%n%B%nCOMMIT_END") >"${CHANGELOG_BUFFER}" ; wait ;

RAW_IMPACTED_ISSUES=$(cat <"${CHANGELOG_BUFFER}" | grep -oE "([#]\d+){1}\b" | sort -id | uniq | xargs -L1 -I{} printf "%s, " "{}" ; wait ;)
RAW_FLAGS_USED=$(cat <"${CHANGELOG_BUFFER}" | grep -oE "^([\[][A-Z]+[]]){1}" | sort -id | uniq -c | sort -rid | grep -oE "([A-Z]+){1}" | xargs -L1 -I{} printf "%s, " "{}" ; wait ;)


# header
printf "%s\n\n" "## What Changed between \`${GIT_RANGE}\`" ;
# insights table
printf "%s\n%s\n" "| Details | |" "|------------------|---------------------|" ;
printf "%s" "| Kinds of changes | " ;
printf "%s\n" "${RAW_FLAGS_USED:-'None'} |" | sed -e 's/,  |/ |/g' ;
printf "%s" "| Impacted Issues | " ;
printf "%s\n" "${RAW_IMPACTED_ISSUES:-'None'} |" | sed -e 's/,  |/ |/g' ;
printf "\n\n" ;

# auto-collect gitlog
for FILE_INPUT in $(git log --pretty=format:"%n" --name-only "${GIT_RANGE}" | sort -id | uniq) ; do

if [[ ( -n "$FILE_INPUT" ) ]] ; then

awk -v RS='' -v ORS='\n\n\n' -v filename="$FILE_INPUT" '
    {
        # Check if the block contains a valid change-log entry
        if ($0 ~ /((Changes in)|(Additions with)|(Deletions from)) file/ && $0 ~ filename) {
            # Ensure that there is no content before the match
            if ($0 ~ /^[[:space:]]*((Changes in)|(Additions with)|(Deletions from))/) {
                # Extract the header (first line) and the content
                header = $0; 
                header_line = substr(header, 1, index(header, ":") - 1);  # Get the header
                if (header_line ~ filename) {
                    content = substr(header, index(header, ":") + 1);  # Get the content after the header
                    # Combine the header and content
                    combined[header_line] = (combined[header_line] ? combined[header_line] "\n" : "") content;
                }
            }
        }
    }
    END {
        # Print combined entries
        for (h in combined) {
            print h ":" combined[h]
        }
    }
' <"${CHANGELOG_BUFFER}" | sort -id | uniq | sort -rd

fi ;

done ;

unset cache 2>/dev/null || : ;

# remove the buffer
rm -f "${CHANGELOG_BUFFER}" 2>/dev/null || : ;
