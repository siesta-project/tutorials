#
# Common aliases
#
#
export BZR_REMOTE_PATH=/usr/bin/bzr
export BZR_EDITOR=emacs
#
## Vesta

if [ -z "${PATH}" ]
then
   PATH="/home/apps/zcam2012/vesta"; export PATH
else
   PATH="/home/apps/zcam2012/vesta:$PATH"; export PATH
fi

## OpenMPI

if [ -z "${PATH}" ]
then
   PATH="$ZCAM/ompi-1.8/bin"; export PATH
else
   PATH="$ZCAM/ompi-1.8/bin:$PATH"; export PATH
fi

## Variables de entorno de jmol, necesarias.

export JMOL_HOME=/home/apps/zcam2014/jmol-14.0.13
if [ -z "${PATH}" ]
then
   PATH="$JMOL_HOME"; export PATH
else
   PATH="$JMOL_HOME:$PATH"; export PATH
fi

#
XCRYSDEN_TOPDIR=/apps/zcam2012/xcrysden
XCRYSDEN_SCRATCH=/tmp
export XCRYSDEN_TOPDIR XCRYSDEN_SCRATCH
PATH="$XCRYSDEN_TOPDIR:$PATH:$XCRYSDEN_TOPDIR/scripts:$XCRYSDEN_TOPDIR/util"
#
COMMON_PATH=$PATH
export COMMON_PATH
#
set -o emacs
set -o noclobber
set -o ignoreeof
#
alias recent="ls -lt | head "
alias gx='gnuplot -persist -display $DISPLAY'
#

alias student="source /home/apps/zcam2014/siesta/config/student.bashrc"
alias prof="source /home/apps/zcam2014/siesta/config/prof.bashrc"
