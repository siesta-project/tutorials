# .bashrc
#
# For some unknown reason, this script must not be used as
# the standard .bashrc in the student account at BIFI...
# Put it in $SIESTA_DIR/config and have students copy it
# to their accounts and source it...
#
#
# Version appropriate for the Siesta Tutorial, 16-19 June 2014
# DO NOT MODIFY without telling Alberto Garcia (albertog@icmab.es)

SYSTEM_PATH=$PATH
export SYSTEM_PATH

SIESTA_DIR=/apps/zcam2014/siesta
export SIESTA_DIR

source ${SIESTA_DIR}/config/common.bashrc

#
# Set "student" profile by default
#

source ${SIESTA_DIR}/config/student.bashrc

