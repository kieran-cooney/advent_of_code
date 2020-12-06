#lang racket
(require racket/string)

(define (read-questions file-path)
  (let* ([s (file->string file-path)]
         [groups-of-strings (string-split s "\n\n")]
         [groups-of-answers (map (lambda (s) (string-split s)) groups-of-strings)])
    groups-of-answers))

(define (combine-answers answers combine-func)
  (apply combine-func
   (map (lambda (l) (apply set l))
    (map string->list answers))))

(define (union-answers answers)
  (combine-answers answers set-union))

(define (intersect-answers answers)
  (combine-answers answers set-intersect))

(define (num-union-answers answers)
  (set-count (union-answers answers)))

(displayln "Test answers")
(define test-answers (read-questions "inputs/6_test.txt"))
(displayln test-answers)
(displayln "Num combined answers per group in test")
(displayln (map (compose set-count union-answers) test-answers))
(displayln "Num common answers per group in test")
(displayln (map (compose set-count intersect-answers) test-answers))

(displayln "Answer to part 1 (Sum of combined answers)")
(define answers (read-questions "inputs/6.txt"))
(displayln (apply + (map num-union-answers answers)))
(displayn "Answer to part 2 (Sum of common answers)")
(displayln (apply + (map (compose set-count intersect-answers) answers)))