#lang racket

;Returns a function checking if the argument is equal to i
(define (equal-to? i)
  (lambda (j) (equal? i j)))

; Check if there is a number in tl that can be added to hd
; to give i
(define (check-sum i hd tl)
  (ormap
   (lambda (x) (equal? x (- i hd)))
   tl))

; Check-sum but then checks if there is any pair of numbers in tl
; summing to i.
(define (valid-number-helper i hd tl)
    (cond
      [(null? tl) #f]
      [(check-sum i hd tl) #t]
      [else (valid-number-helper i (car tl) (cdr tl))]))

(define (valid-number? i xs)
  (if (null? xs)
      #f
      (if (valid-number-helper i (car xs) (cdr xs))
          #t
          (valid-number? i (cdr xs)))))

(define (find-first-invalid-number xs n)
  (if (<= (length xs) n)
      #f     
      (let ([pre-amble (take xs n)]
            [i (list-ref xs n)])
        (if (valid-number? i pre-amble)
            (find-first-invalid-number (cdr xs) n)
            i))))

(define (read-numbers fp)
  (map string->number (file->lines fp)))

(define (sum-min-max-sub-list xs first last)
  (let* ([sub-list (list-tail (take xs (+ last 1)) first)]
         [max-num (apply max sub-list)]
         [min-num (apply min sub-list)])
    (+ max-num min-num)))

(define (find-weakness-helper numbers invalid first last sum)
  (let ([first-val (list-ref numbers first)]
        [last-val (list-ref numbers last)])
    (cond [(equal? sum invalid) (sum-min-max-sub-list numbers first last)]
          [(or (>= first-val invalid) (>= last-val invalid)) -1]
          [(< sum invalid)
           (find-weakness-helper numbers invalid first (+ last 1)
                          (+ sum (list-ref numbers (+ last 1))))]
          [(> sum invalid)
           (find-weakness-helper numbers invalid (+ first 1) last
                          (- sum first-val))]
          [(or (>= first-val invalid) (>= last-val invalid)) -1])))

(define (find-weakness numbers invalid)
  (find-weakness-helper numbers invalid 0 0 (car numbers)))

(displayln "Find first invalid number in test")
(define test-numbers (read-numbers "inputs/9_test.txt"))
(define test-invalid-number (find-first-invalid-number test-numbers 5))
(displayln test-invalid-number)
(displayln "Find test encryption weakness")
(displayln (find-weakness test-numbers test-invalid-number))

(displayln "First invalid number (Answer for part 1)")
(define numbers (read-numbers "inputs/9.txt"))
(define invalid-number (find-first-invalid-number numbers 25))
(displayln invalid-number)
(displayln "Enryption weakness (Answer for part 2)")
(displayln (find-weakness numbers invalid-number))