#!/bin/bash

_RUN="transiesta"
_ts=${RUN-$_RUN}
_tbt=${_ts//transiesta/tbtrans}
_s=${_ts//transiesta/siesta}

trap "echo 'You quitting on me?' ; pwd ; exit 1" SIGINT SIGTERM

cleanTS() {
    local sys=$1 ; shift
    local del_dm=1
    if [ $# -gt 0 ]; then
	local opt=$1 ; shift
	echo "$opt"
	case $opt in
	    -no-DM)
		del_dm=0
		;;
	esac
    fi
    if [ $del_dm -eq 0 ]; then
	[ -e $sys.DM ] && mv $sys.DM old.DM
    fi
    rm $sys.[^f]* fdf-* \
	INPUT_TMP.* 0_* BASIS_* *.ion* \
	CLOCK FORCE_STRESS NON_TR* TIMES \
	${sys}.tbt* *.nc OCCS
    [ -e old.DM ] && cp old.DM $sys.DM
}

runTS() {
    # Grab directory
    local dir=$1 ; shift
    local sys=$1 ; shift
    pushd $dir
    cleanTS $sys $@
    $_ts < $sys.fdf | tee $sys.out
    popd
}

runS() {
    # Grab directory
    local dir=$1 ; shift
    local sys=$1 ; shift
    pushd $dir
    cleanTS $sys $@
    $_s < $sys.fdf > $sys.out
    popd
}

runTBT() {
    # Grab directory
    local dir=$1 ; shift
    local sys=$1 ; shift
    pushd $dir
    $_tbt < $sys.fdf | tee $sys.tbt-out
    popd
}
