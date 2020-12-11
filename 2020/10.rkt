#lang racket

(define (read-adapters fp)
  (sort (map string->number (file->lines fp)) <))

; Dont' need the target argument, as we know target is always
; +3 from the last adapter.
(define (get-jolt-diffs-helper adapters target current diffs)
  (cond [(and (null? adapters) (< current target (+ current 4)))
         (cons (car diffs) (+ (cdr diffs) 1))]
        [(null? adapters) #f]
        [else
         (let* ([hd (car adapters)]
               [tl (cdr adapters)]
               [diff (- hd current)]
               [1-diffs (car diffs)]
               [3-diffs (cdr diffs)])
           (cond [(equal? diff 1)
                  (get-jolt-diffs-helper tl target hd (cons (+ 1-diffs 1) 3-diffs))]
                 [(equal? diff 3)
                  (get-jolt-diffs-helper tl target hd (cons 1-diffs (+ 1 3-diffs)))]))]))

(define (get-jolt-diffs adapters)
  (let ([target (+ (last adapters) 3)]
        [diffs (cons 0 0)])
    (get-jolt-diffs-helper adapters target 0 diffs)))

(define (get-prev-3 lst i)
  (let* ([sub-list (list (- i 3) (- i 2) (- i 1))]
         [sub-list (filter (lambda (x) (>= x 0)) sub-list)]
         [vals (map (lambda (x) (list-ref lst x)) sub-list)]
         [val (list-ref lst i)]
         [zipped (map cons sub-list vals)]
         [zipped (filter (lambda (x) (<= (cdr x) (+ val 3))) zipped)]
         [sub-list (map car zipped)])
    sub-list))

(define (num-arrangements-helper adapters)
  (letrec
      ([rev-adapters (reverse adapters)]
       [memo (cons (cons 0 1) null)]
       [f (lambda (i)
            (let ([ans (assoc i memo)])
              (if ans
                  (cdr ans)
                  (let* ([sub-list (get-prev-3 rev-adapters i)]
                         [new-ans (apply + (map f sub-list))])
                    (begin (set! memo (cons (cons i new-ans) memo)))
                    new-ans))))])
    f))

(define (num-arrangements adapters)
  ((num-arrangements-helper (cons 0 adapters))
   (- (length adapters) 1)))

(define test1-adapters (read-adapters "inputs/10_test1.txt"))
(define test2-adapters (read-adapters "inputs/10_test2.txt"))
(displayln "Difference distribution on test 1")
(displayln (get-jolt-diffs test1-adapters))
(displayln "Difference distribution on test 2")
(displayln (get-jolt-diffs test2-adapters))
(displayln "Num arrangements on tests 1 and 2")
(displayln (num-arrangements test1-adapters))
(displayln (num-arrangements test2-adapters))

(define adapters (read-adapters "inputs/10.txt"))
(displayln "Difference distribution on input")
(define jolt-diffs (get-jolt-diffs adapters))
(displayln jolt-diffs)
(displayln "Product of differences (Answer for part 1)")
(displayln (* (car jolt-diffs) (cdr jolt-diffs)))
(displayln "Number of arrangements (Answer for part 2)")
(displayln (num-arrangements adapters))