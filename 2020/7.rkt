#lang racket
(require racket/string)

(define (truncate-string s i)
  (substring s 0 (- (string-length s) i)))

(define (parse-content-string s)
  (let ([color (cadr (regexp-match #px"^\\d+\\s(.*)\\sbags?\\.?$" s))]
        [i (string->number (cadr (regexp-match #px"^(\\d+).+$" s)))])
    (cons color i)))

(define (parse-contents-string s)
  (if (equal? s "no other bags.")
      null
      (map parse-content-string (string-split s ", "))))


(define (parse-rule rule-string)
  (let* ([container-contents (string-split rule-string "contain")]
         [container-string (string-trim (car container-contents))]
         [container (truncate-string container-string 5)]
         [contents-string (string-trim (cadr container-contents))]
         [contents-list (parse-contents-string contents-string)])
    (cons container contents-list)))

; Should use a helper here
(define (containing-bags rules bags acc)
  (if (null? rules)
      acc
      (let* ([rule (car rules)]
             [tl (cdr rules)]
             [container-color (car rule)]
             [content-pairs (cdr rule)]
             [content-colors (list->set (map car content-pairs))])
        (if (set-member? acc container-color)
            (containing-bags tl bags acc)
            (if (> (set-count (set-intersect bags content-colors)) 0)
                (containing-bags tl bags (set-add acc container-color))
                (containing-bags tl bags acc))))))

(define (all-containing-bags rules bags acc)
  (let ([new-bags (containing-bags rules bags acc)])
    (if (subset? new-bags acc)
        acc
        (all-containing-bags rules new-bags (set-union acc new-bags)))))

;How would you implement tail recursion here?
(define (count-bags rules bag)
  (let ([contents (cdr (assoc bag rules))])
    (if (null? contents)
        0
        (apply +
               (map (lambda (p)
                      (* (cdr p) (+ 1 (count-bags rules (car p)))))
                    contents)))))
        

(displayln "Test rules parsing")
(define test-rules-string (file->lines "inputs/7_test.txt"))
(define test-rules (map parse-rule test-rules-string))
(for-each displayln test-rules)
(displayln "Test containing bags")
(displayln (all-containing-bags test-rules (set "shiny gold") (set)))
(displayln "How many bags does a shiny gold bag contain? (Test)")
(displayln (count-bags test-rules "shiny gold"))

(displayln "Second test")
(define test-rules-string-1 (file->lines "inputs/7_test1.txt"))
(define test-rules-1 (map parse-rule test-rules-string-1))
(displayln "How many bags does a shiny gold bag contain? (Second test)")
(displayln (count-bags test-rules-1 "shiny gold"))

(displayln "Answer for part 1, number of bags which can eventually contain a shiny gold bag")
(define rules (map parse-rule (file->lines "inputs/7.txt")))
(displayln (set-count (all-containing-bags rules (set "shiny gold") (set))))
(displayln "Answer for part 2, ow many bags does a shiny gold bag contain?")
(displayln (count-bags rules "shiny gold"))