program diffv

!calculates the velocity autocorrelation function,

implicit none

integer, parameter :: dp=kind(1.0d0)
real(dp)           :: pi

real(dp), dimension(:,:), allocatable :: xa, xaNext,xaLast  ! input velocities
real(dp), dimension(:), allocatable :: ma  ! atomic mass
real(dp)                                :: Ek, EkCM  ! Kinetic energy 
real(dp), dimension(:,:,:), allocatable :: va! Obtained from xa and time step
integer :: trun, tcor,na,i,j,k,t0,tt0,tt0max,t,nmol,istep,ia,l
integer :: n,m,count,ja, iTime,ix, ntimes,time
real(dp) ::  omega,IR,magn, cell(3,3), cellSize, maxRange, dx,dTime
real(dp) :: Hmass, Omass,  normal, vaCM(3)
complex, dimension(:), allocatable :: aux1,aux2,vcross,ACF,gauss
real(dp), parameter :: Cspeed=3d10 ! cm/s
real(dp), parameter :: Kb=1.38d-23 !J/K
real(dp), parameter :: Temp=300 !K
real(dp), parameter :: hbar=6.626d-34 ! J*s
real(dp), parameter :: fs2s=1e-15 ! 1fs in s
real(dp), parameter :: amu=1.66053892e-27 ! 1 amu in Kg
real(dp), parameter :: ang=1e-10 ! 1 Ang in m
character(len=32):: fname, sysname
character(len=2), dimension(:), allocatable :: spec

pi=acos(-1.0d0)

read(5,*) fname
do ix = 1,3
  read(5,*) cell(:,ix)  ! Unit cell vectors
end do
read(5,*) Hmass, Omass  ! Masses of H (or D) and O atoms (amu)
read(5,*) trun  ! has to be power of 2
read(5,*) dTime

! Find maximum meaningful neighbor distance (half the unit cell size)
  maxRange = minval(sqrt(sum(cell(:,:)**2,dim=1))) / 2


! Find system name
  l = len(trim(fname)) - 4
  sysname = fname(1:l)

! Open .ANI datafile and read number of atoms
  open( unit=1, file=trim(fname), status='old' )
  read(1,*) na                        ! Number of atoms

! Allocate arrays
  allocate(spec(na))
  allocate(xa(na,3))
  allocate(ma(na))
  allocate(xaNext(na,3))
  allocate(xaLast(na,3))
  allocate(va(na,3,0:trun-1))
  allocate(aux1(0:trun-1))
  allocate(aux2(0:trun-1))
  allocate(gauss(0:trun-1))
  allocate(Vcross(0:trun-1))
  allocate(ACF(0:trun-1))

  rewind(unit=1)
  nMol = na/3                         ! Number of water molecules
  ! Read first two geometries
  read(1,*,end=999) na                ! Number of atoms
  do ia = 1,na
    read(1,*) spec(ia),xa(ia,:)       ! Species and cartesian coords.
  end do
  read(1,*,end=999) na
  do ia = 1,na
    read(1,*) spec(ia), xaNext(ia,:)
  end do

! Assign atom masses
  do ia = 1,na
    if (spec(ia)=='O') then
      ma(ia) = Omass
    else if (spec(ia)=='H') then
      ma(ia) = Hmass
    end if
  end do ! ia 


    open(unit=11,file=trim(sysname)//'.EK',status='unknown')
! Loop on time steps, to generate velocities
  nTimes = 0
  do iTime = 1,Trun
    !print*, "reading frame:", iTime
    time = (iTime-1)*dTime

    ! Shift geometry one time step
    xaLast = xa
    xa = xaNext

    ! Read next-time geometry
    read(1,*,end=999) na                   ! Number of atoms
    do ia = 1,na
      read(1,*) spec(ia),xaNext(ia,:)  ! Species and cartes. coords.
    end do
    do ia = 1,na
      dx = sqrt(sum((xaNext(ia,:)-xaLast(ia,:))**2))
      if (dx > maxRange) stop 'ERROR: anomalous position jump'
    end do

    ! Calculate atomic velocities and forces
    ek = 0
    VaCM=0
    do ia = 1,na
      va(ia,:,iTime-1) = (xaNext(ia,:)-xaLast(ia,:)) / (2*dTime)
      VaCM=VaCM+va(ia,:,iTime-1)*ma(ia)
    enddo
    VaCM=VaCM/(sum(ma))
    do ia = 1,na
     ek=ek+0.5d0*ma(ia)*sum(va(ia,:,iTime-1)**2)
    !  fa(:,ia) = ma(ia) * (xaNext(:,ia)-2*xa(:,ia)+xaLast(:,ia)) / dTime**2
    end do
    ekCM=0.5d0*sum(ma)*sum(VaCM**2)
  !  Convert ek to J
    ek=ek*amu*Ang**2/fs2s**2
    ekCM=ekCM*amu*Ang**2/fs2s**2
  ! Convert ek to K
    ek=ek/Kb
    ekCM=ekCM/Kb
    write(11,*) iTime, ek, ekCM
  enddo 
  close(11)

999 continue  !  Exit point when reaching end of file


! Start Autocorrelation

  aux1=0.0d0
  Vcross=0.0d0
  ACF=0.0d0
  ! Normalization counter
  count=0
  normal = 0.0d0
  Do i=1,na
   do j=i,i
     print*, "ia, ja =", i, j
     do l=1,3
! Call to the direct FFT
          aux1=cmplx(va(i,l,:)*sqrt(ma(i)))
          n=size(aux1)
          call four1(aux1,n,-1)
          Vcross=aux1*conjg(aux1)          
! Inverse transform VCross
          call four1(Vcross,n,1)
          Vcross=Vcross/real(size(Vcross))
          ACF = ACF + Vcross
          normal = normal +  (sum(va(i,l,:) * va(j,l,:))*sqrt(ma(i)*ma(j)))/Trun
      enddo
      count=count+1
    enddo
  enddo 
  ! Normalize
  ACF=ACF/real(count*normal)

  aux1=cmplx(ACF)
  call four1(aux1,n,-1)
  open(unit=12,file=trim(sysname)//'.pDOS',status='unknown')
  n=size(aux1)
  Do t=0,n/2-1
    omega=(t/(fs2s*dTime*n))/Cspeed
    magn=sqrt(real(aux1(modulo(t,n)))**2+aimag(aux1(modulo(t,n)))**2)
    IR=magn
    WRITE(12,*) omega, IR
  END DO
  close(12)
end
