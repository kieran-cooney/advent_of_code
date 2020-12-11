#lang racket
; Need to debug. Write functions to print out iterations on test.
(define (file->chairs fp)
  (map string->list (file->lines fp)))

(define (display-chairs chairs)
  (let ([chair-strings (cons "\n" (map list->string chairs))])
    (for-each displayln chair-strings)))

(define (chair-ref chair-row i)
  (if (or (equal? -1 i) (equal? (length chair-row) i))
      #\o
      (list-ref chair-row i)))

(define (get-chair chairs i j)
  (let ([num-rows (length chairs)])
    (if (or (equal? i -1) (equal? i num-rows))
        #\o
        (let ([chair-row (chair-ref chairs i)])
          (chair-ref chair-row j)))))

(define (get-adj-chairs chairs i j)
  (list
   (get-chair chairs (- i 1) (- j 1))
   (get-chair chairs (- i 1) j)
   (get-chair chairs (- i 1) (+ j 1))
   (get-chair chairs i (- j 1))
   (get-chair chairs i (+ j 1))
   (get-chair chairs (+ i 1) (- j 1))
   (get-chair chairs (+ i 1) j)
   (get-chair chairs (+ i 1) (+ j 1))))

(define (occupied? chair)
  (equal? chair #\#))

(define (num-adj-occupied-chairs chairs i j)
  (let ([adj-chairs (get-adj-chairs chairs i j)])
    (length (filter occupied? adj-chairs))))

(define (update-chair chairs i j)
  (let ([chair (get-chair chairs i j)]
        [adj-occ-chairs (num-adj-occupied-chairs chairs i j)])
    (cond [(and (equal? chair #\L) (equal? adj-occ-chairs 0)) #\#]
          [(and (equal? chair #\#) (>= adj-occ-chairs 4)) #\L]
          [else chair])))

(define (update-chair-row chairs i)
  (letrec ([old-chair-row (list-ref chairs i)]
           [row-length (length old-chair-row)]
           [f
            (lambda (j)
              (if (equal? j row-length) null
                  (cons (update-chair chairs i j) (f (+ j 1)))))])
    (f 0)))
  
(define (update-chairs chairs)
  (letrec ([num-rows (length chairs)]
        [f
         (lambda (i)
           (if (equal? i num-rows) null
               (cons (update-chair-row chairs i) (f (+ i 1)))))])
    (f 0)))

(define (get-stable-chairs chairs verbose)
  (let ([new-chairs (update-chairs chairs)]
        [print-func (if verbose display-chairs (lambda (x) void))])
    (begin (print-func chairs)
           (if (equal? chairs new-chairs) chairs
               (get-stable-chairs new-chairs verbose)))))

(define (count-occupied-chairs chairs)
  (length (filter occupied? (flatten chairs))))

(displayln "Test case")
(define test-chairs (file->chairs "inputs/11_test.txt"))
(displayln "Test chairs")
(display-chairs test-chairs)
(displayln "Step through seating process for test case")
(define stable-test-chairs (get-stable-chairs test-chairs #t))
(displayln (count-occupied-chairs stable-test-chairs))

(displayln "Answer for part 1")
(define chairs (file->chairs "inputs/11.txt"))
(define stable-chairs (get-stable-chairs chairs #f))
(displayln (count-occupied-chairs stable-chairs))