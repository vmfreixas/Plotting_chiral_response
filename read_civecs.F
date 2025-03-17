
!--------------------------------------------------------------!
! This program reads civecs binary files as produced by NWChem !      
!--------------------------------------------------------------!

      program test_read_civecs
c
      implicit none 
c
      integer ipol 
      character*256 filename
c
      ipol = 1
c
      filename = 'civecs1.civecs_singlet'
c
      call read_civecs(ipol, filename)
c
      contains
c
         subroutine read_civecs(ipol,filename)
c
         implicit none
c
         integer ipol             !1 for closed shell, 2 for open shell
         character*256 filename
c
         integer i,m,n,k
         logical tda
         integer nroots
         integer nocc(2)
         integer nmo(2)
         integer nfc(2)
         integer nfv(2)
         integer nov(2)
         integer nvir(2)
         integer icntr,itmom
         integer nbf_ao
         integer ok
         double precision r
c        CI vectors are written out as X+Y and X-Y
         double precision, allocatable, dimension(:,:) :: g_x_alpha
         double precision, allocatable, dimension(:,:) :: g_x_beta
         double precision, allocatable, dimension(:,:) :: g_y_alpha
         double precision, allocatable, dimension(:,:) :: g_y_beta

         ok = 0
c
c        Read header information from civecs file
         open(unit=69,file=filename,form='unformatted',
     &          status='unknown',err=1000)
            rewind(69)
            read(69,err=1001) tda
            read(69,err=1001) ipol
            read(69,err=1001) nroots
            read(69,err=1001) nocc(1),nocc(2)
            read(69,err=1001) nmo(1),nmo(2)
            read(69,err=1001) nfc(1),nfc(2)
            read(69,err=1001) nfv(1),nfv(2)
            read(69,err=1001) nov(1),nov(2)
            read(69,err=1001)
c
            if (ipol.eq.1) nocc(2)=0
            if (ipol.eq.1) nmo(2)=0
            if (ipol.eq.1) nfc(2)=0
            if (ipol.eq.1) nfv(2)=0
c
            do i=1,ipol
             nov(i)=(nmo(i)-nfv(i)-nocc(i))*(nocc(i)-nfc(i))
            end do ! ipol
            if (ipol.eq.1) nov(2)=0
         close(unit=69,status='keep',err=1002) ! file
         ok = 1
c
c        Set up X, Y vectors and transition density matrices
         do i=1, ipol
           if (i.eq.1) then
             allocate(g_x_alpha(nroots, nov(i)))
             g_x_alpha = 0.0d0
           endif
           if (i.eq.2) then
             allocate(g_x_beta(nroots, nov(i)))
             g_x_beta = 0.0d0
           endif
           if (.not.tda) then
             if (i.eq.1) then
               allocate(g_y_alpha(nroots, nov(i)))
               g_y_alpha = 0.0d0
             endif
             if (i.eq.2) then
               allocate(g_y_beta(nroots, nov(i)))
             endif
           endif
         enddo
c
c        Read remainder of the civecs file
         open(unit=69,file=filename,form='unformatted',
     &                status='unknown',err=1000)
           rewind(69)
           read(69,err=1001) tda
           read(69,err=1001) ipol
           read(69,err=1001) nroots
           read(69,err=1001) nocc(1),nocc(2)
           read(69,err=1001) nmo(1),nmo(2)
           read(69,err=1001) nfc(1),nfc(2)
           read(69,err=1001) nfv(1),nfv(2)
           read(69,err=1001) nov(1),nov(2)
           read(69,err=1001)
c
           do n = 1, nroots
c
             read(69) r  ! energy of root
             read(69) r  ! s2
c
             do i=1,ipol
c
               if (.not.tda) then
                 if (i.eq.1) then
                   call sread(69, g_x_alpha(n,:), nov(i))
                   call sread(69, g_y_alpha(n,:), nov(i))
                 endif
                 if (i.eq.2) then
                   call sread(69, g_x_beta(n,:), nov(i))
                   call sread(69, g_y_beta(n,:), nov(i))
                 endif     
               else ! tda
                 if (i.eq.1) then
                   call sread(69, g_x_alpha(n,:), nov(i))
                 endif
                 if (i.eq.2) then
                   call sread(69, g_x_beta(n,:), nov(i))
                 endif     
               end if  !tda
             end do ! ipol
         end do ! nroots
c
c        Separate out X and Y vectors if the calculations are not TDA
c        Nothing needs to be done for TDA as Y is zero
         if (.not.tda) then
           do i=1,ipol
             if (i.eq.1) then
               g_x_alpha = 0.5d0 * g_x_alpha + 0.5 * g_y_alpha
               g_y_alpha = g_x_alpha - g_y_alpha
             endif
             if (i.eq.2) then
               g_x_beta = 0.5d0 * g_x_beta + 0.5 * g_y_beta
               g_y_beta = g_x_beta - g_y_beta
             endif
           enddo
         end if

         open(unit = 79, file = 'civecs_1.data')
           nvir(1) = nmo(1) - nocc(1)
           do n = 1, nroots
             write(79, *) 'Root ', n
             write(79, *) 'Nocc ', nocc(1)
             write(79, *) 'Nvir ', nmo(1) - nocc(1)
             do i = 1, nocc(1)
               write(79, '(100000F15.8)') (g_x_alpha(n, m),
     & m = 1 + (i-1) * nvir(1), i * nvir(1))
             enddo
           enddo
         close(69)
c
         return
c
 1000 print *, 'failed to open file'
 1001 print *, 'failed to read file'
 1002 print *, 'failed to close file'
c
         end subroutine read_civecs
c $Id$

      end program test_read_civecs
