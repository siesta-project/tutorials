#---------------------------#
# "Student" profile
#
# Remove any "professor" paths
#
PATH=${COMMON_PATH}
PS1="\h-student> "
#
# Setup for exercises  
#
SIESTA_MASTER=/apps/zcam2014/siesta/SIESTA
. ${SIESTA_MASTER}/Config/tutorial.bashrc
alias update="rsync -av --exclude '.bzr/' ${SIESTA_MASTER} $HOME"
#
