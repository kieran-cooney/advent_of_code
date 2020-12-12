#lang racket

(define (string->instruction s)
  (let* ([s (string-trim s)]
         [action (string-ref s 0)]
         [value (string->number (substring s 1))])
    (cons action value)))

(define (file->instructions fp)
  (map string->instruction (file->lines fp)))

(define directions
  (list #\E #\S #\W #\N))


(define (rotate-ship dir value)
  (let* ([angle (index-of directions dir)]
         [new-angle (+ angle (/ value 90))]
         [new-dir (list-ref directions (modulo new-angle 4))])
    new-dir))

(define (move-ship-compass-dir action value loc)
  (let ([x-loc (car loc)]
        [y-loc (cdr loc)])
    (match action
      [#\N (cons x-loc (+ y-loc value))]
      [#\S (cons x-loc (- y-loc value))]
      [#\E (cons (+ x-loc value) y-loc)]
      [#\W (cons (- x-loc value) y-loc)]
      [_ (raise-argument-error 'move-ship-compass-dir "direction?" action)])))

(define (move-ship-forward value dir loc)
  (move-ship-compass-dir dir value loc))

(define (move-ship-step action value dir loc)
  (cond
    [(member action directions)
     (cons dir (move-ship-compass-dir action value loc))]
    [(equal? action #\F) (cons dir (move-ship-forward value dir loc))]
    [(equal? action #\R) (cons (rotate-ship dir value) loc)]
    [(equal? action #\L) (cons (rotate-ship dir (- value)) loc)]
    [else (raise-argument-error 'move-ship-step "action?" action)]))
         
(define (move-ship-helper instructions dir loc)
  (if (null? instructions)
      loc
      (let* ([instruction (car instructions)]
             [tl (cdr instructions)]
             [action (car instruction)]
             [value (cdr instruction)]
             [new-state (move-ship-step action value dir loc)]
             [new-dir (car new-state)]
             [new-loc (cdr new-state)])
        (move-ship-helper tl new-dir new-loc))))

(define (move-ship instructions)
  (move-ship-helper instructions #\E (cons 0 0)))

(define (manhattan-distance pr)
  (+ (abs (car pr)) (abs (cdr pr))))

(define (loc-negate l1)
  (cons (- (car l1)) (- (cdr l1))))

(define (loc-sum l1 l2)
  (let ([x1 (car l1)] [y1 (cdr l1)]
        [x2 (car l2)] [y2 (cdr l2)])
    (cons (+ x1 x2) (+ y1 y2))))

(define (loc-difference l1 l2)
  (loc-sum l1 (loc-negate l2)))

(define (loc-scale l1 i)
  (cond
    [(equal? i 0) (cons 0 0)]
    [(< i 0) (loc-negate (loc-scale l1 (- i)))]
    [else (loc-sum l1 (loc-scale l1 (- i 1)))]))

(define (move-ship-to-waypoint ship-loc wp-loc i)
  (let* ([diff-loc (loc-scale wp-loc i)]
         [new-ship-loc (loc-sum ship-loc diff-loc)])
    new-ship-loc))

(define (loc-rotate l1 angle)
  (let ([trunc-angle (modulo angle 360)]
        [x (car l1)]
        [y (cdr l1)])
    (match trunc-angle
      [0 l1]
      [90 (cons y (- x))]
      [180 (cons (- x) (- y))]
      [270 (cons (- y) x)]
      [_ (raise-argument-error 'loc-rotate "quarter-angle?" angle)])))

(define (move-ship-waypoint-step action value ship-loc wp-loc)
  (cond
    [(member action directions)
     (cons ship-loc (move-ship-compass-dir action value wp-loc))]
    [(equal? action #\F)
     (cons (move-ship-to-waypoint ship-loc wp-loc value) wp-loc)]
    [(equal? action #\R)
     (cons ship-loc (loc-rotate wp-loc value))]
    [(equal? action #\L)
     (cons ship-loc (loc-rotate wp-loc (- value)))]
    [else (raise-argument-error move-ship-waypoint-step "action?" action)]))

(define (move-ship-waypoint-helper instructions ship-loc wp-loc verbose)
  (if (null? instructions)
      ship-loc
      (let* ([instruction (car instructions)]
             [tl (cdr instructions)]
             [action (car instruction)]
             [value (cdr instruction)]
             [new-state (move-ship-waypoint-step action value ship-loc wp-loc)]
             [new-ship-loc (car new-state)]
             [new-wp-loc (cdr new-state)]
             [print-func (if verbose (lambda p (displayln p)) (lambda (p) void))])
        (begin (print-func (cons new-ship-loc new-wp-loc))
               (move-ship-waypoint-helper tl new-ship-loc new-wp-loc verbose)))))

(define (move-ship-waypoint instructions verbose)
  (move-ship-waypoint-helper instructions (cons 0 0) (cons 10 1) verbose))

(displayln "Ship journey on test")
(define test-instructions (file->instructions "inputs/12_test.txt"))
(define test-final-loc (move-ship test-instructions))
(displayln test-final-loc)
(displayln "Ship waypoint journey on test")
(define test-wp-final-loc (move-ship-waypoint test-instructions #t))
(displayln test-wp-final-loc)

(displayln "Ship journey and manhattan distance (Answer for part 1)")
(define instructions (file->instructions "inputs/12.txt"))
(define final-loc (move-ship instructions))
(displayln final-loc)
(displayln (manhattan-distance final-loc))
(displayln "Ship and waypoint journey with manhattan distance (Answer for part 2)")
(define final-wp-loc (move-ship-waypoint instructions #f))
(displayln (manhattan-distance final-wp-loc))