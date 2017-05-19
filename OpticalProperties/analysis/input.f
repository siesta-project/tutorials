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

C Written by Daniel Sanchez-Portal

       INTEGER*4 NE, NEMX, NSPIN, LASTI,NEXT
       PARAMETER (NEMX=100000)
       REAL*8 E(2),E2(NEMX,2),ESTEP
       REAL*8 OMEGA(NEMX), OMG, eV
       REAL*8 EMAX, EMIN, FSUM(2), THRESHOLD, THRES
       REAL*8 C,P,SUM,A,B, EPSMIN, SUM2 , EMAXP, DRUDE(2)
       PARAMETER (THRESHOLD=0.80)
       PARAMETER (eV= 13.6058d0)     
       PARAMETER (EPSMIN=0.01)
       PARAMETER (EMAXP=200.0d0)
       CHARACTER*3 CHAR
       LOGICAL EXTEND, NONZERO
C
C
C
       READ(5,*) 
       READ(5,'(a,2f10.4)') CHAR, EMIN,EMAX
       write(6,*)  CHAR, EMIN,EMAX
       READ(5,*)
       READ(5,'(a,i3)') CHAR, NSPIN
       write(6,*)  CHAR, NSPIN
       DO ISP=1,NSPIN
          READ(5,*) 
          READ(5,'(a,f10.4)') CHAR, FSUM(ISP)
          write(6,*)  CHAR,FSUM(ISP)
          READ(5,*)
          READ(5,'(a,f10.4)') CHAR, DRUDE(ISP)
          write(6,*)  CHAR, DRUDE(ISP)
       ENDDO 
       DO 10 I=1,NEMX+1
         READ(5,*,END=15) OMG,(E(ISP),ISP=1,NSPIN)
         IF(I.LE.NEMX) THEN
              OMEGA(I)=OMG
              DO ISP=1,NSPIN
                E2(I,ISP)=E(ISP)
              ENDDO   
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
       THRES=THRESHOLD     
       IF((THRES.GT.1.0d0).OR.(THRES.LT.0.0d0)) THEN
          STOP 'threshold must be in the range [0:1]'
       ENDIF

       DO ISP=1,NSPIN
         LASTI=NE
         EMAX=OMEGA(NE)
         EMIN=OMEGA(1)
         EXTEND=.FALSE.
         IF(FSUM(ISP).LT.THRESHOLD) then 
          write(6,'(a,i4,a)') 
     .      'Fsum rule is not fulfilled by more than a',
     .       nint((1.0d0-THRESHOLD)*100.0),'%' 
          write(6,*) 'The dielectric function will be extended'
          write(6,*) 'to higher energies by enforcing the Fsum rule'
          write(6,*) 'This will increase the quality of the quantities'
          write(6,*) 'calculated via the Kramers-Kroning relation'
          EXTEND=.TRUE. 
          SUM=0.0d0
          SUM2=0.0d0 
          NONZERO=.FALSE.
          DO I=NE,1,-1
             IF(.NOT.NONZERO) THEN 
               IF(E2(I,ISP).GT.EPSMIN) THEN
                   NONZERO=.TRUE.
                   LASTI=I
               ENDIF
               SUM2=SUM2+E2(I,ISP)*OMEGA(I)/eV
             ENDIF
             IF(NONZERO) THEN 
               SUM=SUM+E2(I,ISP)*OMEGA(I)/eV
             ENDIF
          ENDDO
          SUM=SUM*ESTEP/eV
          SUM2=SUM2*ESTEP/eV
          A=(SUM+SUM2)/FSUM(ISP)-SUM
          OMGLAST=OMEGA(LASTI)
          P=2.0d0+E2(LASTI,ISP)*(OMGLAST/eV)**2/A
          C=E2(LASTI,ISP)*(OMGLAST/eV)**P
          
          B=SUM*0.01d0/FSUM(ISP)
          EMAX=DLOG(C/((P-2)*B) )/(P-2)
          EMAX=MIN(EMAX*eV,EMAXP)
        ENDIF

         if(NSPIN.eq.1) then 
           open (unit=1,file='e2.dat',status='unknown') 
         else
           if(isp.eq.1) then 
           open (unit=1,file='e2.dat.spin1',status='unknown')
           else
           open (unit=1,file='e2.dat.spin2',status='unknown')
           endif
         endif
          write(1,*) drude(isp)
          do i=1,lasti
            write(1,*) omega(i),e2(i,isp)
         enddo               
         if(extend) then 
          next=nint((emax-omega(lasti))/estep)+1
          do i=1,next
            omg=omega(lasti)+i*estep 
            write(1,*) omg, C/(omg/eV)**p
          enddo 
         endif

       ENDDO 
      
       END
