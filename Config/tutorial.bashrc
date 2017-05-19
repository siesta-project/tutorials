#
#  Bash rc file for Siesta Tutorial 
#
#---------------------------
SIESTA_EXERCISES=$HOME/SIESTA
SIESTA_BIN=${SIESTA_EXERCISES}/bin
export SIESTA_EXERCISES
export SIESTA_BIN
PATH=${SIESTA_BIN}:$PATH
#--------------
#
# CECAM scratch
#
FAST=/disk2/$USER
export FAST
#
#-----Pseudo section
ATOM_UTILS_DIR=${SIESTA_EXERCISES}/Pseudos/Utils
ATOM_PROGRAM=${SIESTA_BIN}/atm
export ATOM_UTILS_DIR
export ATOM_PROGRAM
#
alias ae="sh ${ATOM_UTILS_DIR}/ae.sh"
alias pg="sh ${ATOM_UTILS_DIR}/pg.sh"
alias pt="sh ${ATOM_UTILS_DIR}/pt.sh"
alias energies="grep '&d'"
alias eigenvalues="grep '&v'"
eigenvalues_s () { grep '&v' $1 | grep s ;}
eigenvalues_p () { grep '&v' $1 | grep p ;}
eigenvalues_d () { grep '&v' $1 | grep d ;}
eigenvalues_f () { grep '&v' $1 | grep f ;}
alias gp="gnuplot -persist"
#-----------
#
# To convert WFSX format to WFS
# 
convert_wfs () { ln -sf $1.WFSX WFSX ; wfsx2wfs ; mv WFS $1.WFS ;}
#
#---------------------------
#
# Other useful aliases and definitions
#
set -o emacs
set -o noclobber
set -o ignoreeof
#
alias r="fc -s"
alias gcat="gzip -dc"
alias h='fc -l'
alias j=jobs
alias m=$PAGER
alias ll='ls -lagFo'
alias g='egrep -i'
alias more='/usr/bin/less -c'
#
# # be paranoid
alias cp='cp -ip'
alias mv='mv -i'
alias rm='rm -i'
alias ls='ls -F'
#
pack () { tar cf - $1 | gzip > $1.tgz ;}
hogs () { du -s * | sort -nr | head -10 ;}
grokw () { grep -iw $1 *.{f,F,f90,F90} ;}
#
alias psf="ps xu"
alias psa="ps axu | head -10 | cut -c1-80"
#
alias emacs='emacs -nw'
#
# Work around brain-deadness
#
alias awk='LANG=C LC_ALL=C awk'

