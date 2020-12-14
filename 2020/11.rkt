#lang racket

; Read file to list of list of chars, corresponding to chairs.
(define (file->chairs fp)
  (map string->list (file->lines fp)))

(define (display-chairs chairs)
  (let ([chair-strings (cons "\n" (map list->string chairs))])
    (for-each displayln chair-strings)))

; Get a chair from a chair row
(define (chair-ref chair-row i)
  (if (or (equal? -1 i) (equal? (length chair-row) i))
      #\o
      (list-ref chair-row i)))

; Get a chair from a chair grid
(define (get-chair-with-coords chairs i j)
  (let ([num-rows (length chairs)])
    (if (or (equal? i -1) (equal? i num-rows))
        #\o
        (let ([chair-row (chair-ref chairs i)])
          (chair-ref chair-row j)))))

(define (get-chair chairs loc)
  (get-chair-with-coords chairs (car loc) (cdr loc)))

(define (loc-add l1 l2)
  (cons (+ (car l1) (car l2)) (+ (cdr l1) (cdr l2))))

(define directions
  (list
   (cons -1 -1) (cons -1 0) (cons -1 1)
   (cons 0 -1) (cons 0 1)
   (cons 1 -1) (cons 1 0) (cons 1 1)))

(define (get-adj-locs loc)
  (map (lambda (l) (loc-add loc l)) directions))

(define (get-adj-chairs chairs loc)
  (let ([adj-locs (get-adj-locs loc)])
    (map (lambda (l) (get-chair chairs l)) adj-locs)))

(define (occupied? chair)
  (equal? chair #\#))

(define (get-chair-in-los chairs loc dir)
  (letrec ([f
            (lambda (moving-loc)
              (let* ([new-loc (loc-add moving-loc dir)]
                     [new-chair (get-chair chairs new-loc)])
                (if (equal? new-chair #\.)
                    (f new-loc)
                    new-chair)))])
    (f loc)))

(define (get-all-chairs-by-los chairs loc)
  (map (lambda (dir) (get-chair-in-los chairs loc dir)) directions))

(define (num-adj-occupied-chairs chairs loc)
  (let ([adj-chairs (get-adj-chairs chairs loc)])
    (length (filter occupied? adj-chairs))))

(define (num-los-occupied-chairs chairs loc)
  (let ([los-chairs (get-all-chairs-by-los chairs loc)])
    (length (filter occupied? los-chairs))))

(define (update-chair-by-adj chairs loc)
  (let ([chair (get-chair chairs loc)]
        [adj-occ-chairs (num-adj-occupied-chairs chairs loc)])
    (cond [(and (equal? chair #\L) (equal? adj-occ-chairs 0)) #\#]
          [(and (equal? chair #\#) (>= adj-occ-chairs 4)) #\L]
          [else chair])))

(define (update-chair-by-los chairs loc)
  (let ([chair (get-chair chairs loc)]
        [los-occ-chairs (num-los-occupied-chairs chairs loc)])
    (cond [(and (equal? chair #\L) (equal? los-occ-chairs 0)) #\#]
          [(and (equal? chair #\#) (>= los-occ-chairs 5)) #\L]
          [else chair])))

(define (update-chair-row chairs i update-func)
  (letrec ([old-chair-row (list-ref chairs i)]
           [row-length (length old-chair-row)]
           [f
            (lambda (j)
              (if (equal? j row-length) null
                  (cons (update-func chairs (cons i j)) (f (+ j 1)))))])
    (f 0)))
  
(define (update-chairs chairs update-func)
  (letrec ([num-rows (length chairs)]
        [f
         (lambda (i)
           (if (equal? i num-rows) null
               (cons (update-chair-row chairs i update-func) (f (+ i 1)))))])
    (f 0)))

(define (get-stable-chairs chairs update-func verbose)
  (let ([new-chairs (update-chairs chairs update-func)]
        [print-func (if verbose display-chairs (lambda (x) void))])
    (begin (print-func chairs)
           (if (equal? chairs new-chairs) chairs
               (get-stable-chairs new-chairs update-func verbose)))))

(define (get-stable-adj-chairs chairs verbose)
  (get-stable-chairs chairs update-chair-by-adj verbose))


(define (get-stable-los-chairs chairs verbose)
  (get-stable-chairs chairs update-chair-by-los verbose))

(define (count-occupied-chairs chairs)
  (length (filter occupied? (flatten chairs))))

(displayln "Test case")
(define test-chairs (file->chairs "inputs/11_test.txt"))
(displayln "Test chairs")
(display-chairs test-chairs)
(displayln "Step through seating process for test case")
(define stable-adj-test-chairs (get-stable-adj-chairs test-chairs #t))
(displayln (count-occupied-chairs stable-adj-test-chairs))
(displayln "Test chairs for line of sight rules")
(define stable-los-test-chairs (get-stable-los-chairs test-chairs #t))
(displayln (count-occupied-chairs stable-los-test-chairs))

(displayln "Answer for part 1")
(define chairs (file->chairs "inputs/11.txt"))
(define stable-adj-chairs (get-stable-adj-chairs chairs #f))
(displayln (count-occupied-chairs stable-adj-chairs))
(displayln "Answer for part 2")
(define stable-los-chairs (get-stable-los-chairs chairs #f))
(displayln (count-occupied-chairs stable-los-chairs))