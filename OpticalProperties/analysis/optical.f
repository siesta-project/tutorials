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
C  This program calculates several optical properties
C  out of the imaginary part of the dielectric
C  function using the Kramers-Kroning relations
C   Written by Pablo Ordejon
C   Modified by DSP, December 2000
C   Modified by DSP, January  2006


       COMMON /EPSILON/ E1,E2
       COMMON /ENERGY/ OMEGA,NE
       INTEGER*4 NE, NEMX
       PARAMETER (NEMX=100000)
       REAL*8 E,E1(NEMX),E2(NEMX),ESTEP
       REAL*8 K,OMEGA(NEMX),REFL,N, OMG
       REAL*8 LAMBDA, COND, drude, gamm
       LOGICAL DRUD
C  FROM eV to cm**-1
       PARAMETER (LAMBDA=8067.422)
C   from eV to (meter*ohm)**-1 (conductivity)
       PARAMETER (COND=13445.4)
C
C
C
       DRUD=.false.
       GAMM=0.0d0
       OPEN(UNIT=7,FILE='e2.dat',status='unknown')
       READ(7,*) DRUDE
       DO 10 I=1,NEMX+1
         READ(7,*,END=15) OMG,E
         IF(I.LE.NEMX) THEN
              OMEGA(I)=OMG
              E2(I)=E
         ELSE
           STOP 'Too many frequency points'
         ENDIF
10     CONTINUE
15     NE=I-1
       CLOSE(7)

       ESTEP=OMEGA(2)-OMEGA(1)
       DO 20 I=3,NE
          IF (DABS(ESTEP - (OMEGA(I)-OMEGA(I-1))).GT. 1.D-4) THEN
             STOP 'Energy grid is not regular'
          ENDIF
20     ENDDO
C
C
       OPEN(UNIT=8,FILE='e1.interband.out',status='unknown')
       DO 100 I=1,NE
          E=OMEGA(I)
          CALL INTEG1(E,K)
          K=2.0D0/(4.0D0*DATAN(1.0D0))*K
          E1(I)=K
          WRITE(8,*) E,1.0d0+K
100    CONTINUE
       CLOSE(8)
C
C

       OPEN(UNIT=8,FILE='e2.interband.out',status='unknown')
       DO 110 I=1,NE
          E=OMEGA(I)
          CALL INTEG2(E,K)
           K=-2.0D0/(4.0D0*DATAN(1.0D0))*K*E
          WRITE(8,*) E,K
110    CONTINUE
       CLOSE(8)
      
       DO I=1,NE
          E1(I)=1.0d0+E1(I)
       ENDDO

C      Drude term?
       IF(DRUDE.gt.1.0d-4) THEN
       WRITE(6,*) "Do you want to include a Drude term?"
       WRITE(6,*) "This is typically needed for metals"
       WRITE(6,*) "if yes: enter 1, if no: enter 0"
       READ(5,*) i
       IF(I.eq.1) THEN
         DRUD=.true.
       ELSEIF(I.eq.0) THEN
         DRUD=.false.
       ELSE
          stop "not a valid answer"
       ENDIF
       
       if(DRUD) then 
         WRITE(6,*) "We need an empirical relaxation time"
         WRITE(6,*) "Enter the invers in Ha units"
         READ(5,*) gamm
         IF(gamm.eq.0.0d0) gamm=1.0d-10
         OPEN(UNIT=7,FILE='e1.Drude.out',status='unknown')
         OPEN(UNIT=8,FILE='e2.Drude.out',status='unknown')
         do i=1,ne
             e=omega(i)/13.6058d0
             e1(i)=e1(i) - drude/(e**2+gamm**2)
             e2(i)=e2(i) + gamm*drude/(e+1.0d-20)/(e**2+gamm**2)    
             write(7,*) omega(i), -drude/(e**2+gamm**2)
             write(8,*) omega(i), gamm*drude/(e+1.0d-20)/(e**2+gamm**2)
         enddo
         CLOSE(7)
         CLOSE(8) 
       endif
       ENDIF
       
C
       OPEN(UNIT=14, FILE='epsilon_real.out', status='unknown')
       OPEN(UNIT=15, FILE='epsilon_img.out',status='unknown')
       OPEN(UNIT=9,FILE='refrac_index.out',status='unknown')
       OPEN(UNIT=10,FILE='absorp_index.out',status='unknown')
       OPEN(UNIT=11,FILE='reflectance.out',status='unknown')
C  ABSORPTION COEFFICIENT IN cm**-1
       OPEN(UNIT=12,FILE='absorp_coef.out',status='unknown')
C  OPTICAL  CONDUCTIVITY IN (ohm*m)**-1
       OPEN(UNIT=13,FILE='conductivity.out',status='unknown')
         
       DO 120 I=1,NE
           K=DSQRT((DSQRT(E1(I)**2+E2(I)**2)-E1(I))/2.0D0)
           N=DSQRT((DSQRT(E1(I)**2+E2(I)**2)+E1(I))/2.0D0)
           REFL=((N-1)**2+K**2)/(((N+1)**2+K**2))
          WRITE(14,*) OMEGA(I), E1(I)
          WRITE(15,*) OMEGA(I), E2(I)
          WRITE(9,*)  OMEGA(I),N
          WRITE(10,*) OMEGA(I),K
          WRITE(11,*) OMEGA(I),REFL
          WRITE(12,*) 
     .     OMEGA(I), OMEGA(I)*LAMBDA*K*(16.0D0*DATAN(1.0D0))
          WRITE(13,*) OMEGA(I),COND*OMEGA(I)*E2(I)
120    CONTINUE
       CLOSE(9)
       CLOSE(10)
       CLOSE(11)
       CLOSE(12)
       CLOSE(13)
       CLOSE(14)
       CLOSE(15)


       STOP
       END
C
C
       SUBROUTINE INTEG1(E,K)
C
       COMMON /ENERGY/ OMEGA,NE
       REAL*8 E,EP,F,K,FAC
       REAL*8 OMEGA(100000)
       INTEGER*4 NE,I
C
       K=0.0D0
       DO 10 I=1,NE
C
          EP=OMEGA(I)
C
          CALL FUNC1(I,E,EP,F)
C
          IF (I .EQ. 1) THEN
             FAC=1.0D0/3.0D0
             GOTO 100
          END IF
          IF (I .EQ. NE) THEN
             FAC=1.0D0/3.0D0
             GOTO 100
          END IF
          II=I/2
          II=II*2
          IF (II .EQ. I) THEN
             FAC=4.D0/3.D0
             GOTO 100
          END IF
          FAC=2.D0/3.D0
100       CONTINUE
C
          K=K+FAC*F
10     CONTINUE
C
C
C
C
       K=K*(OMEGA(2)-OMEGA(1))
C
C
       RETURN
       END
C
C
C
       SUBROUTINE FUNC1(I,E,EP,F)
C
       COMMON /ENERGY/ OMEGA,NE
       COMMON /EPSILON/ E1,E2
       REAL*8 E,EP,F,E1(100000),E2(100000)
       REAL*8 OMEGA(100000)
       INTEGER*4 IEP,NE,I
C
C
       F=0.0D0
C
C
C
       IF (E .EQ. EP) THEN
       F=0.0D0
       GOTO 1000
       ENDIF
       F=EP*E2(I)/(EP**2-E**2)
C
C
1000   CONTINUE
C
C
C
       RETURN
       END

       SUBROUTINE INTEG2(E,K)
C
       COMMON /ENERGY/ OMEGA,NE
       REAL*8 E,EP,F,K,FAC
       REAL*8 OMEGA(100000)
       INTEGER*4 NE,I
C
       K=0.0D0
       DO 10 I=1,NE
C
          EP=OMEGA(I)
C
          CALL FUNC2(I,E,EP,F)
C
          IF (I .EQ. 1) THEN
             FAC=1.0D0/3.0D0
             GOTO 100
          END IF
          IF (I .EQ. NE) THEN
             FAC=1.0D0/3.0D0
             GOTO 100
          END IF
          II=I/2
          II=II*2
          IF (II .EQ. I) THEN
             FAC=4.D0/3.D0
             GOTO 100
          END IF
          FAC=2.D0/3.D0
100       CONTINUE
C
          K=K+FAC*F
10     CONTINUE
C
C
       K=K*(OMEGA(2)-OMEGA(1))
C
C
       RETURN
       END
C
C
C
       SUBROUTINE FUNC2(I,E,EP,F)
C
       COMMON /ENERGY/ OMEGA,NE
       COMMON /EPSILON/ E1,E2
       REAL*8 E,EP,F,E1(100000),E2(100000)
       REAL*8 OMEGA(100000)
       INTEGER*4 IEP,NE,I
C
C
       F=0.0D0
C
C
C
       IF (E .EQ. EP) THEN
       F=0.0D0
       GOTO 1000
       ENDIF
       F=E1(I)/(EP**2-E**2)
C
C
1000   CONTINUE
C
C
C
       RETURN
       END
