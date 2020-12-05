#lang racket


(define (seat_id->binary seat_id)
  (let* ([id-with-0s (regexp-replace* #px"(L|F)" seat_id "0")]
         [id-with-1s (regexp-replace* #px"(R|B)" id-with-0s "1")]
         [bin-string (string-append "#b" id-with-1s)]
         [num (string->number bin-string)])
    num))

(define (get-missing-int xs)
  (cond
    [(null? xs) 0]
    [(null? (cdr xs)) (car xs)]
    [#t
     (let* ([hd (car xs)]
            [neck (cadr xs)]
            [tl (cdr xs)])
       (if (equal? neck (+ hd 1))
           (get-missing-int tl)
           (+ hd 1)))]))

(displayln "Test cases for first part")

(define test_cases
  (list
   "BFFFBBFRRR"
   "FFFBBBFRRR"
   "BBFFBBFRLL"))

(displayln (map seat_id->binary test_cases))

(displayln "Max seat id (Answer for part 1)")
(define boarding_passes (file->lines "inputs/5.txt"))
(define seat_ids (map seat_id->binary boarding_passes))
(displayln (apply max seat_ids))

(displayln "Missing seat id (Answer for part 2)")
(displayln (get-missing-int (sort seat_ids <)))