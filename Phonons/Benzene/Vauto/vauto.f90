program diffv

!calculates the velocity autocorrelation function,

implicit none

real*8, dimension(:,:,:), allocatable :: va
real*8, dimension(:,:), allocatable :: xa
integer :: trun, tcor,na,i,j,k,initstep,t0,tt0,tt0max,t,nmol,istep
real*8, dimension(:,:), allocatable :: ACF
real*8, dimension(:,:), allocatable :: va0
character*20 :: fileinp,fileout
real*8, dimension(:), allocatable :: anorm,ACFtot
real*8 :: ANOR,timestep
real*8, dimension(3) :: vcm,vcm0


open(unit=1, file="inputV.dat", form="formatted", status="unknown")

read(1,*) fileinp
read(1,*) fileout
read(1,*) initstep
read(1,*) trun
read(1,*) tcor
read(1,*) timestep
read(1,*) na

close(1)

nmol=na
allocate(va(3,nmol,trun))
allocate(xa(3,nmol))
allocate(va0(3,nmol))
allocate(ACF(nmol,0:tcor))
allocate(ACFtot(0:tcor))
allocate(anorm(0:tcor))


open(unit=1, file=fileinp, form="unformatted", status="unknown")
do i=1,initstep-1
  read(1) istep
enddo
do i=1,trun
  read(1) istep, xa(:,:), va(:,:,i)
  write(6,*) istep
enddo

close(1)

ACF=0.0d0
anorm=0.0d0
DO t0=1,trun,100
  write(6,*) t0
  tt0max = MIN( trun, t0 + TCOR)
  DO tt0 = t0, tt0max
    vcm=0.0d0
    do i=1,nmol
      do j=1,3
        vcm(j)=vcm(j)+va(j,i,tt0)
      enddo
    enddo
    vcm=vcm/nmol
    if(tt0.eq.t0) then
      va0=va(:,:,t0)
      vcm0=vcm
    endif
    t = tt0 - t0
    Do i=1,nmol
      do j=1,3
        ACF(i,t)=ACF(i,t) +(va0(j,i)-vcm0(j))*(va(j,i,tt0)-vcm(j))
      enddo
      ACFtot(t) = ACFtot(t) + ACF(i,t)
      ANORM(t)=ANORM(t) + 1.0
    enddo
  enddo
enddo 



       ANOR = ACFtot(0)/ANORM(0)
       open(unit=11, file=fileout, form="formatted", status="unknown")
       DO t =  0, TCOR
          ACFtot(t)  = ACFtot(t)/ANORM(t)
          WRITE(11,*)  t*timestep, ACFtot(t)
       END DO
close(11)

end
