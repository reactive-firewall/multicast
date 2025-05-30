#! /bin/bash

function id_current_tag() {
	local INPUT="${1}"
	git describe --tags --abbrev=0 ${INPUT}
}

function enumerate_tag_history() {
	local HEAD_TAG=$(id_current_tag HEAD)
	{ git rev-list --tags --ancestry-path "$(git tag --no-contains "${HEAD_TAG}" | sort -V | head -n1)^..HEAD" ; wait ;} | xargs -I{} git tag --points-at "{}" 2>/dev/null ;
	wait ;
}

# step 1: is designed to determine the current and previous Git tags and
# then construct a Git range based on these tags. If no argument is provided, it defaults to
# using the tags.
if [[ -z "${1}" ]] ; then
GIT_CURRENT_TAG=$(id_current_tag)
GIT_PREVIOUS_TAG=$(enumerate_tag_history | grep -A 1 -F -f <(git describe --tags --abbrev=0 "${GIT_CURRENT_TAG}") | tail -n1 )
FALLBACK_GIT_RANGE="${GIT_CURRENT_TAG}...${GIT_PREVIOUS_TAG}"
fi ;
GIT_RANGE="${1:-${FALLBACK_GIT_RANGE}}"

# cache the git log
CHANGELOG_BUFFER=".chagelog_buffer.txt"
cat <(git log "${GIT_RANGE}" --reverse --pretty=format:"COMMIT_START%n%h%n%B%nCOMMIT_END") >"${CHANGELOG_BUFFER}" ; wait ;

printf "%s\n\n" "## What Changed between \`${GIT_RANGE}\`" ;

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

# remove the buffer
rm -f "${CHANGELOG_BUFFER}" 2>/dev/null || : ;
