#!/usr/bin/env bash
A1='2'
A2='21'
B1='41'
B2='61'
WHITE='38;2;255;255;255'
GREEN='38;2;0;255;0'
#
#function pcol(){
#	printf '\x1b[%sm %s\x1b[m\n' $2 $1
#}
#function ptab(){
#	printf '\x1b[%sG %s' $2 $1
#}
#VERSION=$(cat pyproject.toml|rg -i version|tr -d 'version = ')
#PROJ=$(basename $PWD)
#L1="$(printf '%s' "$(ptab "$(pcol '| Project:'     '"$WHITE"' )" '"$A1"' ) $(ptab $(pcol '"| Version:"' '"$WHITE"') '"$B1"')) "
#L2="$(printf '%s' "$(ptab "$(pcol '| Upgrading:'   '"$WHITE"' )" '"$A1"' ))"
#L3="$(printf '%s' "$(ptab "$(pcol '| Tests:'       '"$WHITE"' )" '"$A1"' ) $(ptab $(pcol '"| Result:"' '"$WHITE"') '"$B1"'))"
#L4="$(printf '%s' "$(ptab "$(pcol '| Building:'    '"$WHITE"' )" '"$A1"' ))"
#L5="$(printf '%s' "$(ptab "$(pcol '| GIT:'         '"$WHITE"' )" '"$A1"' ))"
#L6="$(printf '%s' "$(ptab "$(pcol '| Stage:'       '"$WHITE"' )" '"$B1"' ))"
#L7="$(printf '%s' "$(ptab "$(pcol '| Commit:'      '"$WHITE"' )" '"$B1"' ))"
#L8="$(printf '%s' "$(ptab "$(pcol '| Push:'        '"$WHITE"' )" '"$B1"' ))"
##L9=$(printf '%s' "$(ptab $(pcol |PYPI (main):" $WHITE) $A1) $(ptab $(pcol "| Uploading:" $WHITEaaaaa) $B1))"
#printf '%s\n %s\n %s\n %s\n %s\n %s\n%s\n%s\n%s\n' $L{1..9}
#
#A1='2'
#B1='41'
#WHITE='38;2;255;255;255'

function pcol() {
    printf '\x1b[%sm%s\x1b[m' "$2" "$1"
}

function ptab() {
    printf '\x1b[%sG' "$1"
}

VERSION=$(cat pyproject.toml | rg -i version | tr -d 'version = ')
PROJ=$(basename "$PWD")

L1="$(ptab "$A1")$(pcol '| Project:          ' "$WHITE")$(ptab "$B1")$(pcol '| Version:          ' "$WHITE")"
L2="$(ptab "$A1")$(pcol '| Upgrading:        ' "$WHITE")"
L3="$(ptab "$A1")$(pcol '| Tests:            ' "$WHITE")$(ptab "$B1")$(pcol '| Result:           ' "$WHITE")"
L4="$(ptab "$A1")$(pcol '| Building:         ' "$WHITE")"
L5="$(ptab "$A1")$(pcol '| GIT:              ' "$WHITE")"
L6="$(ptab "$B1")$(pcol '| Stage:            ' "$WHITE")"
L7="$(ptab "$B1")$(pcol '| Commit:           ' "$WHITE")"
L8="$(ptab "$B1")$(pcol '| Push:             ' "$WHITE")"

printf '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' "$L1" "$L2" "$L3" "$L4" "$L5" "$L6" "$L7" "$L8"


ptab $C1B 32 $PROJ
ptab $C2B 32 $VERSION
echo

pip install --upgrade setuptools &>/dev/null
pip install --upgrade build &>/dev/null
pip install --upgrade twine &>/dev/null
ptab $C1B 32 "DONE"
echo
python -m unittest &> .STATUS_TESTS
[[ -n $(cat .STATUS_TESTS|rg -i '^OK$') ]] && TESTSTATUS='OK' || TESTSTATUS='FAIL'
rm .STATUS_TESTS
ptab $C1B $DONE
ptab $C2A 'Result'
ptab $C2B 32 $TESTSTATUS
echo
ptab  $C1A 'Building Project:'
python -m build &>/dev/null
ptab $C1B $DONE
ptab $C1A 'GIT'
ptab $C2A 'Staging:'
git add . &>/dev/null
ptab $C2B $DONE
printf '\n'
ptab $C2A 'Committing:'
echo "CURRENT VERSION: $VERSION :: TESTS: $TESTSTATUS :: CHANGED: " > .GITCOMMIT_MESSAGE
git status &>> .GITCOMMIT_MESSAGE &>/dev/null
git commit -m "$(cat .GITCOMMIT_MESSAGE)" &>/dev/null
ptab $C2B $DONE
ptab $C2A 'Pushing:'
git push &>/dev/null
ptab $C2B $DONE
printf '\n'
ptab $C1A "Pypi:"
ptab $C2A "Uploading:"

#twine upload  dist/* --verbose  --skip-existing  -u '__token__' -p "$(cat .PYPI_APIKEY)" &>/dev/null
ptab $C2B $DONE

printf '\n________________________________________________________________________________\n________________________________________________________________________________\n\n'
