! 
! This file is part of the SIESTA package.
!
! Copyright (c) Fundacion General Universidad Autonoma de Madrid:
! E.Artacho, J.Gale, A.Garcia, J.Junquera, P.Ordejon, D.Sanchez-Portal
! and J.M.Soler, 1996-2006.
! 
! Use of this software constitutes agreement with the full conditions
! given in the SIESTA license, as signed by all legitimate users.
!
module m_orbital_chooser
!
! Determines which orbitals to consider when processing PDOS data
!
type, public :: orbital_id_t
   integer  :: n
   integer  :: l
   integer  :: m
   integer  :: z
   integer  :: index
   integer  :: atom_index
   character(len=40)  :: species
end type orbital_id_t

public :: want_orbital

CONTAINS

function want_orbital(orbid) result(wantit)
type(orbital_id_t), intent(in)   :: orbid
logical                          :: wantit

!
!  Examples
!  
!  1. Want only s-orbitals
!
!     wantit = ( orbid%l == 0 )
!
!  2. Want only n=3 orbitals
!
!     wantit = ( orbid%n == 3 )
!
!  2. Want 3p orbitals
!
!     wantit = ( ( orbid%n == 3 ) .and. (orbid%l == 0 ) )
!
!  3. Want Oxygen orbitals
!
!     wantit = ( orbid%species == "O" )
!
!wantit = .true.
!
      wantit = ( ( orbid%n == 2 ) .and. (orbid%l == 1 )   &
                 .and. (orbid%m == -1 ) )

end function want_orbital

end module m_orbital_chooser
