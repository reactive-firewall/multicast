#! /bin/bash
# Disclaimer of Warranties.
# A. YOU EXPRESSLY ACKNOWLEDGE AND AGREE THAT, TO THE EXTENT PERMITTED BY
#    APPLICABLE LAW, USE OF THIS SHELL SCRIPT AND ANY SERVICES PERFORMED
#    BY OR ACCESSED THROUGH THIS SHELL SCRIPT IS AT YOUR SOLE RISK AND
#    THAT THE ENTIRE RISK AS TO SATISFACTORY QUALITY, PERFORMANCE, ACCURACY AND
#    EFFORT IS WITH YOU.
#
# B. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THIS SHELL SCRIPT
#    AND SERVICES ARE PROVIDED "AS IS" AND “AS AVAILABLE”, WITH ALL FAULTS AND
#    WITHOUT WARRANTY OF ANY KIND, AND THE AUTHOR OF THIS SHELL SCRIPT'S LICENSORS
#    (COLLECTIVELY REFERRED TO AS "THE AUTHOR" FOR THE PURPOSES OF THIS DISCLAIMER)
#    HEREBY DISCLAIM ALL WARRANTIES AND CONDITIONS WITH RESPECT TO THIS SHELL SCRIPT
#    SOFTWARE AND SERVICES, EITHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT
#    NOT LIMITED TO, THE IMPLIED WARRANTIES AND/OR CONDITIONS OF
#    MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE,
#    ACCURACY, QUIET ENJOYMENT, AND NON-INFRINGEMENT OF THIRD PARTY RIGHTS.
#
# C. THE AUTHOR DOES NOT WARRANT AGAINST INTERFERENCE WITH YOUR ENJOYMENT OF THE
#    THE AUTHOR's SOFTWARE AND SERVICES, THAT THE FUNCTIONS CONTAINED IN, OR
#    SERVICES PERFORMED OR PROVIDED BY, THIS SHELL SCRIPT WILL MEET YOUR
#    REQUIREMENTS, THAT THE OPERATION OF THIS SHELL SCRIPT OR SERVICES WILL
#    BE UNINTERRUPTED OR ERROR-FREE, THAT ANY SERVICES WILL CONTINUE TO BE MADE
#    AVAILABLE, THAT THIS SHELL SCRIPT OR SERVICES WILL BE COMPATIBLE OR
#    WORK WITH ANY THIRD PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES,
#    OR THAT DEFECTS IN THIS SHELL SCRIPT OR SERVICES WILL BE CORRECTED.
#    INSTALLATION OF THIS THE AUTHOR SOFTWARE MAY AFFECT THE USABILITY OF THIRD
#    PARTY SOFTWARE, APPLICATIONS OR THIRD PARTY SERVICES.
#
# D. YOU FURTHER ACKNOWLEDGE THAT THIS SHELL SCRIPT AND SERVICES ARE NOT
#    INTENDED OR SUITABLE FOR USE IN SITUATIONS OR ENVIRONMENTS WHERE THE FAILURE
#    OR TIME DELAYS OF, OR ERRORS OR INACCURACIES IN, THE CONTENT, DATA OR
#    INFORMATION PROVIDED BY THIS SHELL SCRIPT OR SERVICES COULD LEAD TO
#    DEATH, PERSONAL INJURY, OR SEVERE PHYSICAL OR ENVIRONMENTAL DAMAGE,
#    INCLUDING WITHOUT LIMITATION THE OPERATION OF NUCLEAR FACILITIES, AIRCRAFT
#    NAVIGATION OR COMMUNICATION SYSTEMS, AIR TRAFFIC CONTROL, LIFE SUPPORT OR
#    WEAPONS SYSTEMS.
#
# E. NO ORAL OR WRITTEN INFORMATION OR ADVICE GIVEN BY THE AUTHOR
#    SHALL CREATE A WARRANTY. SHOULD THIS SHELL SCRIPT OR SERVICES PROVE DEFECTIVE,
#    YOU ASSUME THE ENTIRE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
#
#    Limitation of Liability.
# F. TO THE EXTENT NOT PROHIBITED BY APPLICABLE LAW, IN NO EVENT SHALL THE AUTHOR
#    BE LIABLE FOR PERSONAL INJURY, OR ANY INCIDENTAL, SPECIAL, INDIRECT OR
#    CONSEQUENTIAL DAMAGES WHATSOEVER, INCLUDING, WITHOUT LIMITATION, DAMAGES
#    FOR LOSS OF PROFITS, CORRUPTION OR LOSS OF DATA, FAILURE TO TRANSMIT OR
#    RECEIVE ANY DATA OR INFORMATION, BUSINESS INTERRUPTION OR ANY OTHER
#    COMMERCIAL DAMAGES OR LOSSES, ARISING OUT OF OR RELATED TO YOUR USE OR
#    INABILITY TO USE THIS SHELL SCRIPT OR SERVICES OR ANY THIRD PARTY
#    SOFTWARE OR APPLICATIONS IN CONJUNCTION WITH THIS SHELL SCRIPT OR
#    SERVICES, HOWEVER CAUSED, REGARDLESS OF THE THEORY OF LIABILITY (CONTRACT,
#    TORT OR OTHERWISE) AND EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE
#    POSSIBILITY OF SUCH DAMAGES. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION
#    OR LIMITATION OF LIABILITY FOR PERSONAL INJURY, OR OF INCIDENTAL OR
#    CONSEQUENTIAL DAMAGES, SO THIS LIMITATION MAY NOT APPLY TO YOU. In no event
#    shall THE AUTHOR's total liability to you for all damages (other than as may
#    be required by applicable law in cases involving personal injury) exceed
#    the amount of five dollars ($5.00). The foregoing limitations will apply
#    even if the above stated remedy fails of its essential purpose.
################################################################################

ulimit -t 1200
PATH="/bin:/sbin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:${PATH}"
# shellcheck disable=SC2086
LANG=${LANG:-"en_US"}
LC_ALL="${LANG:0:5}.utf-8"
umask 137

# Function to check if a command exists.

# USAGE:
#	~$ check_command CMD
# Arguments:
# CMD (Required) -- Name of the command to check
# Results:
#	exits 64 -- missing required argument
#	exits 126 -- check complete and has failed, can not find given command.
#	returns successful -- check complete and command found to be executable.
function check_command() {
	test -z "$1" && { printf "%s\n" "Error: command name is required to check for existence." >&2 ; exit 64 ; } ;
	local cmd="$1" ;
	# shellcheck disable=SC2086
	test -x "$(command -v ${cmd})" || { printf "%s\n" "Error: Required command '$cmd' is not found." >&2 ; exit 126 ; } ;
}  # end check_command()
# propagate/export function to sub-shells
export -f check_command

# Check required commands
check_command awk ;
check_command cat ;
check_command cut ;
check_command git ;
check_command grep ;
check_command head ;
check_command sed ;
check_command sort ;
check_command tail ;
check_command tee ;
check_command tr ;
check_command uniq ;
check_command xargs ;

# rest of the script vars
LOG_FILE="chglog_generation_${PPID}.log"
ERR_FILE="chglog_generation_errors_${PPID}.log"
LOCK_FILE="${TMPDIR:-/tmp}/org.pak.multicast.chglog-generation-shell"
EXIT_CODE=0

# USAGE:
#	~$ id_current_tag INPUT_HINT_FOR_CURRENT
# Arguments:
#	INPUT (Required) -- Hint reference for the current tag to retrieve (e.g., HEAD or current SHA)
# Results:
#	returns the most recent tag associated with the current commit.
function id_current_tag() {
	local INPUT_HINT_FOR_CURRENT="${1}"
	git describe --tags --abbrev=0 ${INPUT_HINT_FOR_CURRENT}
}  # end id_current_tag()

# USAGE:
#	~$ run_enumerate_tag_history
# Results:
#	returns a list of tags that are ancestors of the current HEAD, excluding the current tag.
function run_enumerate_tag_history() {
	local HEAD_TAG=$(id_current_tag HEAD)
	{ git rev-list --tags --ancestry-path "$(git tag --no-contains "${HEAD_TAG}" | sort -V | head -n1)^..HEAD" ; wait ;} | xargs -I{} git tag --points-at "{}" 2>/dev/null ;
	wait ;
}  # end run_enumerate_tag_history()

# USAGE:
#	~$ enumerate_tag_history
# Results:
#	returns a cached list of tags that are ancestors of the current HEAD, excluding development tags.
#	If the cache is empty, it populates the cache by calling run_enumerate_tag_history.
function enumerate_tag_history() {
	if [[ -z "${cache}" ]] ; then
		cache=$(run_enumerate_tag_history | grep -vE "v?\d+.\d+.\d+-dev" ; wait;)
	fi ;
	printf "%s\n" "${cache}" ;
	wait ;
}  # end enumerate_tag_history()

# USAGE:
#	~$ id_parent_tag INPUT
# Arguments:
#	INPUT (Required) -- The tag or commit to find the parent tag for
# Results:
#	returns the parent tag of the specified input tag or commit.
function id_parent_tag() {
	local INPUT="${1}"
	enumerate_tag_history | grep -A 1 -F -f <(id_current_tag ${INPUT} ) | tail -n1
	wait ;
}  # end id_parent_tag()

# step 1: is designed to determine the current and previous Git tags and
# then construct a Git range based on these tags. If no argument is provided, it defaults to
# using the tags.
if [[ -z "${1}" ]] ; then
	# GIT_CURRENT_TAG=$(id_current_tag)
	printf "# Changelog\n" ;
	for EACH_TAG in $(enumerate_tag_history | sort -Vr) ; do
		GIT_PREVIOUS_TAG=$(id_parent_tag "${EACH_TAG}")
		if [[ ( -n "${GIT_PREVIOUS_TAG}" ) ]] && [[ ( "${EACH_TAG}" != "${GIT_PREVIOUS_TAG}" ) ]] ; then
			FALLBACK_GIT_RANGE="${EACH_TAG}...${GIT_PREVIOUS_TAG}"
			"${0}" "${FALLBACK_GIT_RANGE}" || : ; wait ;
		fi ;
	done;
	unset FALLBACK_GIT_RANGE 2>/dev/null || : ;
	unset GIT_PREVIOUS_TAG 2>/dev/null || : ;
	exit 0 ;
fi ;
GIT_RANGE="${1}"

# cache the git full log
CHANGELOG_BUFFER="${TMPDIR:-/tmp}/.chagelog_buffer.txt"
cat <(git log "${GIT_RANGE}" --reverse --pretty=format:"COMMIT_START%n%h%n%B%nCOMMIT_END") >"${CHANGELOG_BUFFER}" ; wait ;

RAW_FLAGS_LIST=$(cat <"${CHANGELOG_BUFFER}" | grep -oE "([\[][A-Z]+[]]){1}" | sort -id | uniq -c | sort -rid | grep -oE "([A-Z]+){1}" | sort -id | uniq | sort -rd ; wait ;)

RAW_IMPACTED_ISSUES=$(cat <"${CHANGELOG_BUFFER}" | grep -oE "([#]\d+){1}\b" | sort -id | uniq | xargs -L1 -I{} printf "%s, " "{}" ; wait ;)
RAW_FLAGS_USED=$(cat <(printf "%s\n" "${RAW_FLAGS_LIST}") | xargs -L1 -I{} printf "%s, " "{}" ; wait ;)
RAW_NEW_FILES=$(cat <"${CHANGELOG_BUFFER}" | grep -F "Additions with file" | sort -id | cut -d\  -f4- | sort -id | uniq -c | tr -s ' ' ' ' | cut -d\  -f 3- | cut -d: -f 1-1 | xargs -L1 -I{} printf "%s, " "{}" ; wait ;)
RAW_DEL_FILES=$(cat <"${CHANGELOG_BUFFER}" | grep -F "Deletions from file" | sort -id | cut -d\  -f4- | sort -id | uniq -c | tr -s ' ' ' ' | cut -d\  -f 3- | cut -d: -f 1-1 | xargs -L1 -I{} printf "%s, " "{}" ; wait ;)


# header
printf "%s\n\n" "## What Changed between \`${GIT_RANGE}\`" ;
# insights table
printf "%s\n%s\n" "| Details | |" "|------------------|---------------------|" ;
printf "%s" "| Kinds of changes | " ;
printf "%s\n" "${RAW_FLAGS_USED:-'None'} |" | sed -e 's/,  |/ |/g' ;
printf "%s" "| Impacted Issues | " ;
printf "%s\n" "${RAW_IMPACTED_ISSUES:-'None'} |" | sed -e 's/,  |/ |/g' ;
if [[ ( -n "${RAW_NEW_FILES}" ) ]] ; then
	printf "%s" "| New Files | " ;
	printf "%s\n" "${RAW_NEW_FILES:-'None'} |" | sed -e 's/,  |/ |/g' ;
fi ;
if [[ ( -n "${RAW_DEL_FILES}" ) ]] ; then
	printf "%s" "| Removed Files | " ;
	printf "%s\n" "${RAW_DEL_FILES:-'None'} |" | sed -e 's/,  |/ |/g' ;
fi ;

if [[ ( ${VERBOSE_CHANGE_LOG:-0} -gt 0 ) ]] ; then
# flags sub-header
printf "\n### Changes by Kind\n" ;

# cache the git log summaries with hashes
CHANGELOG_BUFFER_SHORT="${TMPDIR:-/tmp}/.short chagelog_buffer.txt"
cat <(git log "${GIT_RANGE}" --reverse --grep="([\[][A-Z]+[]]){1}" -E --pretty=format:"COMMIT_START%n%h %s%nCOMMIT_END") >"${CHANGELOG_BUFFER_SHORT}" ; wait ;

# auto-collect by flags
for FLAG_ID in $(printf "%s\n" "${RAW_FLAGS_LIST}") ; do

if [[ ( -n "$FLAG_ID" ) ]] ; then

awk -v RS='\n' -v ORS='\n\n\n' -v flagname="$FLAG_ID" '
    {
        # Check if the block contains a valid change-log entry
        if ($0 ~ /([\[][A-Z]+[]]){1}/ && $0 ~ flagname) {
            # Ensure that there is no content before the match
            if ($0 ~ /^[a-f0-9]{7,7}[[:space:]]*(([\[][A-Z]+[]]){1})/) {
                # Extract the header (first line) and the content
                header = $0;
                hash_line = substr(header, 1, 7);  # Get the hash
                header_line = substr(header, index(header, "[") + 1, (index(header, "]") - index(header, "[")) - 1);  # Get the header
                if (header_line ~ flagname) {
                    content = " * " hash_line " --" substr(header, index(header, "]") + 1);  # Get the content after the header
                    # Combine the header and content
                    combined[header_line] = (combined[header_line] ? combined[header_line] "\n" : "") content;
                }
            }
        }
    }
    END {
        # Print combined entries
        for (h in combined) {
            print h ":\n" combined[h]
        }
    }
' <"${CHANGELOG_BUFFER_SHORT}" | sort -id | uniq | sort -id -k 4

fi ;

done ;

rm -f "${CHANGELOG_BUFFER_SHORT}" 2>/dev/null || : ;
# files sub-header
printf "\n### Changes by file\n" ;
else
# NO sub-headers
printf "\n\n" ;
fi ;

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
# diff link
printf "**Full Changelog**: %s(%s)\n\n***\n\n" "[\`${GIT_RANGE}\`]" \
"https://github.com/reactive-firewall/multicast/compare/${GIT_RANGE}" ;

# cleanup
unset RAW_NEW_FILES 2>/dev/null || : ;
unset RAW_IMPACTED_ISSUES 2>/dev/null || : ;
unset RAW_FLAGS_USED 2>/dev/null || : ;
unset GIT_RANGE 2>/dev/null || : ;
unset cache 2>/dev/null || : ;

# remove the buffer
rm -f "${CHANGELOG_BUFFER}" 2>/dev/null || : ;

exit ${EXIT_CODE:-255} ;
