#lang racket
(require racket/string)

;Import file to string
;Split string on \n\n
;Split strings on spaces
;Split strings on : into pairs
;Check if valid

(define required-fields
  (list "byr" "iyr" "eyr" "hgt" "hcl" "ecl" "pid"))

(define (valid-year lower upper)
  (lambda (s)
    (if (regexp-match-exact? #px"^\\d{4}$" s)
         (let ([d (string->number s)])
           (and (>= d lower) (<= d upper)))
         #f)))

(define (valid-height s)
  (if (regexp-match-exact? #px"^(\\d*)(in|cm)$" s)
      (let* ([match (regexp-match #px"^(\\d*)(in|cm)$" s)]
             [h (string->number (cadr match))]
             [units (caddr match)])
        (case units
          [("cm") (and (>= h 150) (<= h 193))]
          [("in") (and (>= h 59) (<= h 76))]
          [else #f]))
      #f))

(define (regexp-match-exact-func re)
  (lambda (s) (regexp-match-exact? re s)))

(define field-tests
  (list
   (cons "byr" (valid-year 1920 2002))
   (cons "iyr" (valid-year 2010 2020))
   (cons "eyr" (valid-year 2020 2030))
   (cons "hgt" valid-height)
   (cons "hcl" (regexp-match-exact-func #px"^#[a-f\\d]{6}$"))
   (cons "ecl" (regexp-match-exact-func #px"^(amb|blu|brn|gry|grn|hzl|oth)$"))
   (cons "pid" (regexp-match-exact-func #px"^\\d{9}$"))
   (cons "cid" (lambda (s) #t))))

(define (load-passports filepath)
  (let* ([file-string (file->string filepath)]
         [passport-strings (string-split file-string "\n\n")]
         [passport-lists (map string-split passport-strings)]
         [split-passport-string (lambda (s) (string-split s ":"))]
         [split-passport-list (lambda (l) (map split-passport-string l))]
         [passport-pairs (map split-passport-list passport-lists)])
    passport-pairs))

(define (valid-passport passport-pairs)
  (let ([fields (list->set (map car passport-pairs))])
    (if (subset? (list->set required-fields) fields) 1 0)))

(define (valid-passport-values passport-pairs)
  (if (null? passport-pairs)
      #t
      (let* ([hd (car passport-pairs)]
             [tl (cdr passport-pairs)]
             [field (car hd)]
             [value (cadr hd)]
             [valid-value? (cdr (assoc field field-tests))])
        (if (valid-value? value)
            (valid-passport-values tl)
            #f))))

(define (valid-passport-values-verbose passport-pairs)
  (if (null? passport-pairs)
      null
      (let* ([hd (car passport-pairs)]
             [tl (cdr passport-pairs)]
             [field (car hd)]
             [value (cadr hd)]
             [valid-value? (cdr (assoc field field-tests))])
        (cons (list field value (valid-value? value))
              (valid-passport-values-verbose tl)))))
      

(define (valid-passport-2 passport-pairs)
  (if (and (equal? (valid-passport passport-pairs) 1)
           (valid-passport-values passport-pairs))
      1 0))

(displayln "Load test passports")
(define test-passports (load-passports "inputs/4_test.txt"))
(map displayln test-passports)
(displayln "Check test passports")
(map displayln (map valid-passport test-passports))

(displayln "Number of passports with valid fields")
(define passports (load-passports "inputs/4.txt"))
(displayln (apply + (map valid-passport passports)))

(displayln "Invalid test passports")
(displayln (map valid-passport-2 (load-passports "inputs/4_test1.txt")))

(displayln "Invalid test passports verbose")
(map displayln (map valid-passport-values-verbose (load-passports "inputs/4_test1.txt")))


(displayln "Valid test passports")
(displayln (map valid-passport-2 (load-passports "inputs/4_test2.txt")))

(displayln "Number of passports with valid fields and values")
(displayln (apply + (map valid-passport-2 passports)))