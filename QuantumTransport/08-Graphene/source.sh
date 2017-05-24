
# This will create a function that changes the k-grid
# block to a new one

BNAME=TBT.k

_tbtkgrid_help() {
    echo "Run the command: "
    echo "   tbtkgrid"
    echo "for help."
    echo "Call the command with this:"
    echo "   tbtkgrid <filename> <nk>"
    echo "or"
    echo "   tbtkgrid <filename> <kx> <ky>"
}
    
tbtkgrid() {
    [ $# -eq 0 ] && _tbtkgrid_help && return 1
    # Grap file:
    local f=$1 ; shift
    echo "Will change k-grid in '$f' to"
    [ $# -eq 0 ] && _tbtkgrid_help && return 1
    # Get number of k-points
    local x=$1 ; shift
    local y=$x
    [ $# -gt 0 ] && y=$1 && shift
    echo "        kx = $x    ky = $y"
    # Find it it exists
    local saved=0
    rm .tmp
    while IFS='' read -r line
    do 
	local tmp="`echo $line | grep -i "$BNAME"`"
	if [ ! -z "${tmp}" ]; then
	    read -r line
	    read -r line
	    read -r line
	    read -r line
	    saved=1
	    {
		echo "%block $BNAME"
		echo " $x 0 0 0."
		echo " 0 $y 0 0."
		echo " 0 0 1 0."
		echo "%endblock $BNAME" 
	    } >> .tmp
	    continue
	fi
	echo $line >> .tmp
    done < $f
    if [ $saved -eq 0 ]; then
	{
	    echo "%block $BNAME"
	    echo " $x 0 0 0."
	    echo " 0 $y 0 0."
	    echo " 0 0 1 0."
	    echo "%endblock $BNAME"
	} >> .tmp
    fi
    cp .tmp $f
    echo "K-grid block in $f:"
    grep -A 4 "%block $BNAME" $f
}
_tbtkgrid_help

