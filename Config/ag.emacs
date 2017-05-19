(set-input-mode nil nil 1)
(standard-display-european t)
;; 
(keyboard-translate ?\C-h ?\C-?)
(keyboard-translate ?\C-? ?\C-h)

(define-key ctl-x-map "l" 'goto-line)
;;
(setq fill-column 72)
;;
;;;(autoload 'sgml-mode "psgml" "Major mode to edit SGML files." t )
(autoload 'f90-mode "f90"
     "Major mode for editing Fortran 90 code in free format." t)
(setq auto-mode-alist (append auto-mode-alist 
                           (list '("\\.f90$" . f90-mode))))
(setq auto-mode-alist (append auto-mode-alist 
                           (list '("\\.F90$" . f90-mode))))

;;
;; Special files
;;
(setq auto-mode-alist (cons '("\.tes$" . tex-mode) auto-mode-alist))
;;
(setq auto-mode-alist (cons '("\.h$" . fortran-mode) auto-mode-alist))
(setq auto-mode-alist (cons '("\.F$" . fortran-mode) auto-mode-alist))
;
;;
(put 'eval-expression 'disabled nil) 
(setq text-mode-hook (list
      (function (lambda () (auto-fill-mode 1)))))
