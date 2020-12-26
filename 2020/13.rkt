#lang racket
(require math)

(define (get-bus-id s)
  (if (equal? s "x") -1 (string->number s)))

(define (string->bus-ids s)
  (map get-bus-id (string-split s ",")))

(define (file->time-bus-ids fp)
  (let* ([strings (file->lines fp)]
         [first_time (string->number (car strings))]
         [bus_ids (string->bus-ids (cadr strings))])
    (cons first_time bus_ids)))

(define (get-remainders first-time bus-ids)
  (if (null? bus-ids)
      null
      (let ([bus-id (car bus-ids)]
            [tl (cdr bus-ids)])
        (if (> bus-id 0)
            (cons (cons bus-id (- bus-id (modulo first-time bus-id))) (get-remainders first-time tl))
            (get-remainders first-time tl)))))

(define (compare-time-bus-ids pr1 pr2)
  (if (<= (cdr pr1) (cdr pr2))
      pr1
      pr2))

(define (get-earliest-bus first-time bus-ids)
  (let* ([remainders (get-remainders first-time bus-ids)]
         [first-bus (foldl compare-time-bus-ids (car remainders) (cdr remainders))])
  first-bus))

(define (product-pr  pr)
  (* (car pr) (cdr pr)))

(define (get-earliest-time-2  bus-ids)
  (letrec ([f
            (lambda (t d r tl)
              (cond
                [(null? tl) t]
                [(equal? (car tl) -1) (f t d (- r 1) (cdr tl))]
                [#t
                 (let* ([new-d (car tl)]
                        [new-tl (cdr tl)]
                        [new-r (modulo (- r t) new-d)]
                        [d-inv (modular-inverse d new-d)]
                        [m (modulo (* d-inv new-r) new-d)]
                        [new-t (+ t (* m d))])
                   (f new-t (* d new-d) (- r 1) new-tl))]))])
  (f 0 1 0 bus-ids)))

                

(displayln "Test case - first bus")
(define test-time-bus-ids (file->time-bus-ids "inputs/13_test.txt"))
(define test-first-time (car test-time-bus-ids))
(define test-bus-ids (cdr test-time-bus-ids))
(define test-earliest-bus-pr (get-earliest-bus test-first-time test-bus-ids))
(displayln test-earliest-bus-pr)
(displayln (product-pr test-earliest-bus-pr))
(displayln test-bus-ids)
(displayln "Test answer for part 2")
(displayln (get-earliest-time-2 test-bus-ids))

(displayln "Answer for part 1")
(define time-bus-ids (file->time-bus-ids "inputs/13.txt"))
(define first-time (car time-bus-ids))
(define bus-ids (cdr time-bus-ids))
(define earliest-bus-pr (get-earliest-bus first-time bus-ids))
(displayln earliest-bus-pr)
(displayln (product-pr earliest-bus-pr))
(displayln "Answer for part 2")
(displayln (get-earliest-time-2 bus-ids))