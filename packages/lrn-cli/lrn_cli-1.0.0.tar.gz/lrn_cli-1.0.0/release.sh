#!/bin/bash -e

VERSION_FILE="src/_version.py"
CHANGELOG="ChangeLog.md"
GITHUB_BASE_URL="https://github.com/Learnosity/lrn-cli"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SED=$(which gsed || which sed)

check_git_clean () {
	if [[ $(git status --porcelain | wc -l) -gt 0 ]]; then
            echo -e "${RED}Working directory not clean; please add/commit, \`make clean\` and/or \`git clean -fdx\`\n${NC}"
            git status
            exit 1
	fi
}

expect_yes() {
	if ! [[ "${prompt}" =~ [yY](es)* ]]
	then
		echo -e "${RED}Aborting ...${NC}"
		return 1
	fi
	return 0
}

check_version () {
	version="$1"
	if ! [[ "${version}" =~ ^v[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(-[a-z]+\.[0-9]+)?$ ]]
	then
	    echo -e "\\n${RED}Version ${version} does not match semver (vM.m.r[-rc.n])${NC}"
	    return 1
	else
	    return 0
	fi
}

confirm_branch () {
	current_branch=$(git rev-parse --abbrev-ref HEAD)
	echo -ne "${BLUE}"
	read -rp "Do you want to tag the current branch (${current_branch})? <y/N> " prompt
	echo -e "${NC}"
	if ! expect_yes; then
		echo -e "${RED}Please checkout the correct branch and retry.${NC}"
		exit 1
	fi
}

list_last_tags () {
	n_tags=5
	echo -e "${YELLOW}Last ${n_tags} tags:${NC}"
	git tag --sort=tag | tail -n $n_tags
}

get_new_version () {
	# Get new version to release
	echo -ne "${BLUE}"
	read -rp "What version do you want to release? " new_version
	echo -e "${NC}"
	while ! check_version "$new_version"; do
	    read -rp "New version: " new_version
	done
	check_version "${new_version}"
}

print_release_notes () {
	# Print release notes
	echo -e "\\n${YELLOW}Release notes: ${NC}"

	changelog=$(${SED} -n '/Unreleased/,/^## /{/^## /d;p}' "${CHANGELOG}")
	echo -e "${changelog}"
}

confirm_tagging () {
	# prompt to continue
	echo -ne "${BLUE}"
	read -rp "Are you sure you want to update the version and tag? <y/N> " prompt
	echo -e "${NC}"
	expect_yes || exit 1
}

update_version () {
	# update and commit local version file used by tracking telemetry
	echo -e "\\n${YELLOW}Writing version file ...${NC}"
	${SED} -i "s/^__version__ *=.*/__version__ = \"${new_version/v/}\"/" ${VERSION_FILE}

	echo -e "${YELLOW}Updating ${CHANGELOG} ...${NC}"
	${SED} -i "s/^## \[Unreleased]$/&\n\n## [${new_version}] - $(date +%Y-%m-%d)/" "${CHANGELOG}"

	echo -e "${YELLOW}Committing release files ...${NC}"
        git add "${VERSION_FILE}" "${CHANGELOG}"
	git commit --allow-empty -m "[RELEASE] ${new_version}"
}

create_tag () {
	echo -e "\\n${YELLOW}Tagging ...${NC}"
	git tag -a "${new_version}" -m "[RELEASE] ${new_version}" \
		-m "Changes:" -m "${changelog}"
}

confirm_push () {
	# prompt to continue
	echo -ne "${BLUE}"
	read -rp "Are you sure you want to push the new tag? <y/N> " prompt
	echo -e "${NC}"
	if ! expect_yes; then
		revert_tag
	fi
}

push_tag () {
	# push commit and tag
	git push origin "${current_branch}" || revert_tag
	git push origin tag "${new_version}" || revert_tag
}

test() {
	make test || revert_tag
}

test_dist() {
	make dist || revert_tag
}

revert_tag() {
	echo -e "\\n${YELLOW}Reverting tag ...${NC}"
	git tag -d "${new_version}"
	git reset HEAD^
	exit 1
}

handle_package_manager () {
	# script or instructions to push to package manager
	echo -e "\\n${BLUE}Visit ${GITHUB_BASE_URL}/releases/${new_version} and select 'Create release from tag'.\\nUse the following ChangeLog:${NC}"
	echo -e "---8<---\\n\\n${changelog}\\n\\n--->8---"

	echo -ne "${BLUE}"
	read -rp "Done?"
	echo -e "${NC}"
	echo -e "${GREEN}lrn-cli ${new_version} is now released!${NC}"
}

check_git_clean
confirm_branch
list_last_tags
get_new_version
print_release_notes
confirm_tagging
update_version
create_tag
test
test_dist
confirm_push
push_tag
handle_package_manager
