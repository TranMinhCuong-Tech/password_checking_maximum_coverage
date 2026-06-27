# Wiki: Password Checking Maximum Coverage

## 1. Mục đích của tài liệu

Tài liệu này mô tả đầy đủ dự án `password_checking_maximum_coverage` theo đúng cách dự án đang hoạt động trong mã nguồn.

Mục tiêu của project là:

- biến một bài toán kiểm tra / so khớp password thành một bài toán tối ưu tổ hợp
- dùng bài toán **Maximum Coverage** để chọn đúng `k` rules tốt nhất
- so sánh nhiều hướng giải khác nhau, từ brute force đến ILP và heuristic
- giữ code đủ rõ để có thể dùng làm bài học về độ phức tạp thuật toán

Trong phiên bản hiện tại:

- `real_passwords.txt` có 500 password thật
- `mutated_passwords.txt` có 1500 password biến đổi
- `rules.py` định nghĩa 20 rules
- mọi solver đều làm việc trên cùng một biểu diễn tập phủ bằng `set` và `frozenset`

---

## 2. Dữ liệu đầu vào của project

### 2.1. `real_passwords.txt`

Đây là tập password thật, tức là tập vũ trụ cần được phủ.

Ví dụ vài dòng đầu trong file:

```text
123456
123456789
qwerty
password
111111
```

Trong cách mô hình hóa của project, mỗi password thật tương ứng với một phần tử của universe `U`.

### 2.2. `mutated_passwords.txt`

Đây là tập password đích để so khớp.

Ví dụ vài dòng đầu:

```text
abc
!~!11
55555576
Money1
princess
```

Khi một rule được áp lên một password thật và sinh ra một candidate nằm trong tập mutated, password thật đó được tính là “covered”.

### 2.3. Quy mô dữ liệu hiện tại

Theo dữ liệu hiện có trong repo:

- số password thật: 500
- số password mutated: 1500
- số rules: 20

Tỷ lệ này đủ lớn để:

- thấy rõ sự chồng lặp giữa các tập phủ
- làm brute force trở nên đắt hơn khi `k` tăng
- vẫn đủ nhỏ để chạy được nhiều thuật toán trong môi trường học thuật

---

## 3. Ý tưởng tổng quát của project

Project không đơn thuần là “check password đúng hay sai”.

Ý tưởng thật sự là:

1. Mỗi rule là một phép biến đổi chuỗi
2. Với mỗi password thật, áp rule đó để tạo candidate
3. Nếu candidate có mặt trong `mutated_passwords.txt`, password thật đó được coi là được phủ bởi rule
4. Mỗi rule trở thành một tập con các password thật
5. Chọn đúng `k` rules sao cho hợp của các tập con là lớn nhất

Nói ngắn gọn:

- universe `U` = tập password thật
- mỗi rule `i` sinh ra tập con `S_i`
- mục tiêu là chọn `k` tập sao cho `|S_1 ∪ S_2 ∪ ... ∪ S_k|` là lớn nhất

Đây chính là bài toán **Maximum Coverage**.

---

## 4. Lý thuyết nền tảng

### 4.1. NP là gì

Một bài toán thuộc lớp NP nếu lời giải ứng viên của nó có thể được kiểm tra trong thời gian đa thức.

Trong project này, nếu ai đó đưa ra một tập `k` rules, ta có thể kiểm tra tập đó bằng cách:

- lấy union của các tập phủ tương ứng
- đếm số password thật được phủ

Việc kiểm tra một nghiệm cho trước là nhanh hơn nhiều so với việc tự tìm nghiệm tối ưu.

### 4.2. Ví dụ NP ngay trên project

Giả sử người dùng đưa ra nghiệm:

- rule 2: `identity_medium`
- rule 4: `capitalize`
- rule 6: `append_single_digit`

Để kiểm tra nghiệm này, ta chỉ cần:

1. lấy ba tập phủ tương ứng
2. hợp chúng lại
3. đếm số password được phủ

Trong dữ liệu hiện tại, ba rule này phủ được `296 / 500` password thật.

Việc xác minh kết quả này nhanh hơn rất nhiều so với việc thử toàn bộ tổ hợp 3 rules trong 20 rules.

### 4.3. NP-Hard là gì

Một bài toán NP-Hard là bài toán có độ khó ít nhất bằng mọi bài toán trong NP.

Ý nghĩa thực tế:

- nếu ta có thể giải nhanh một bài toán NP-Hard tổng quát
- thì nhiều bài toán NP khác cũng sẽ bị kéo theo

Trong project này, Maximum Coverage là một bài toán NP-Hard kinh điển.

### 4.4. Vì sao Maximum Coverage phù hợp với project

Mô hình của project rất khớp với Maximum Coverage:

- mỗi password thật là một phần tử của universe
- mỗi rule là một tập con các password thật mà rule đó có thể phủ
- nếu hai rules phủ trùng một password, password đó vẫn chỉ được đếm một lần
- mục tiêu là chọn `k` rules tốt nhất

Điểm quan trọng là:

- các tập phủ có thể chồng lặp mạnh
- chọn thêm một rule không có nghĩa là số phần tử phủ tăng tương ứng
- bài toán không chỉ là “rule nào phủ nhiều nhất”, mà là “tập `k` rules nào phủ nhiều nhất khi xét overlap”

### 4.5. Ví dụ chồng lặp từ dữ liệu thật

Một số password trong dữ liệu hiện tại được nhiều rule phủ cùng lúc.

Ví dụ:

```text
qwerty -> được phủ bởi 7 rules
password -> được phủ bởi 6 rules
```

Với `qwerty`, các rule phủ được gồm:

- `identity_short`
- `capitalize`
- `append_single_digit`
- `append_double_digit`
- `append_123`
- `leet_e3`
- `mixed_leet`

Với `password`, các rule phủ được gồm:

- `capitalize`
- `append_single_digit`
- `prepend_single_digit`
- `leet_a4`
- `leet_o0`
- `leet_s$`

Điều này cho thấy:

- một password có thể nằm trong nhiều tập phủ
- coverage của project là union của các tập, không phải tổng đơn giản

### 4.6. Ví dụ chuyển đổi cụ thể từ project

Dưới đây là vài ví dụ đúng với rules hiện có:

| Rule | Ví dụ đầu vào | Candidate sinh ra |
| --- | --- | --- |
| `append_single_digit` | `123456789` | `1234567890` |
| `append_123` | `qwerty` | `qwerty123` |
| `prepend_123` | `1234567890` | `1231234567890` |
| `reverse` | `123456789` | `987654321` |
| `leet_o0` | `password` | `passw0rd` |
| `duplicate_last_char` | `111111` | `1111111` |

Những candidate như vậy chính là cầu nối giữa rule transformation và tập mutated.

### 4.7. Tại sao không cần bitmask

Project này từng có mô tả bitmask trong tài liệu cũ, nhưng code hiện tại không dùng bitmask số nguyên để biểu diễn tập phủ.

Thay vào đó:

- `set` được dùng để tính union nhanh và rõ
- `frozenset` được dùng để memoization hoặc lưu trạng thái bất biến
- số phần tử phủ được tính bằng `len(...)`

Lợi ích của cách này là:

- dễ đọc hơn bitmask
- dễ giải thích với người học
- vẫn giữ được ý tưởng tổ hợp và độ phức tạp cốt lõi

---

## 5. Mô hình hóa toán học trong project

### 5.1. Universe và tập con

Gọi:

- `U` là tập toàn bộ password thật
- `m = |U| = 500`
- `R` là tập 20 rules

Với mỗi rule `r_i`, ta định nghĩa tập phủ:

```text
S_i = { password_j in U | rule i có thể sinh ra ít nhất một candidate nằm trong mutated_passwords }
```

Mục tiêu:

```text
maximize |S_i1 ∪ S_i2 ∪ ... ∪ S_ik|
subject to chọn đúng k rules
```

### 5.2. Biểu diễn trong code

Trong `coverage_problem.py`:

- `build_rule_coverages(passwords)` xây dựng `rule_coverages`
- `rule_coverages[rule_id]` là một `frozenset` chứa chỉ số các password thật được phủ bởi rule đó
- `password_to_rules[index]` là danh sách các rule có thể phủ password đó

Từ đây, mọi solver đều chỉ cần thao tác trên các tập chỉ số.

### 5.3. Ví dụ coverage set theo dữ liệu hiện tại

Một vài rule có coverage lớn nhất trong dữ liệu hiện tại:

- `append_single_digit`: 155 password
- `identity_medium`: 138 password
- `prepend_single_digit`: 96 password
- `duplicate_last_char`: 86 password
- `reverse`: 83 password
- `append_123`: 82 password
- `prepend_123`: 81 password
- `capitalize`: 79 password

Điều này cho thấy:

- không phải rule nào cũng “mạnh” như nhau
- quy tắc sinh thêm ký tự ở cuối hoặc đầu thường phủ được nhiều password
- các rule kiểu biến đổi đơn giản thường đóng vai trò mạnh trong Maximum Coverage

---

## 6. Kiến trúc file trong project

### 6.1. `__init__.py`

Đây là điểm vào của ứng dụng.

Chức năng:

- in banner
- hiển thị file input
- hỏi người dùng chọn `k`
- gọi menu thuật toán

Luồng chính:

```text
showBanner()
-> printRuleCatalog()
-> prompt_k()
-> pwd_checking.runAlgorithms(k, PASSWORD_FILES)
```

### 6.2. `pwd_checking.py`

Đây là bộ điều phối menu thuật toán.

Chức năng:

- load dữ liệu password
- hiển thị menu thuật toán
- map lựa chọn số sang module tương ứng
- gọi `solve_max_coverage(k, password_data)`

Các lựa chọn hiện có:

- Greedy
- Randomized Search
- Hill Climbing
- Local Search
- Beam Search
- Dynamic Programming
- ILP + PuLP + CBC
- Lagrangian Relaxation

### 6.3. `rules.py`

Đây là nơi định nghĩa 20 rules.

Mỗi rule có:

- `name`
- `label`
- `transform`

Ví dụ:

- `append_single_digit`
- `reverse`
- `leet_o0`
- `duplicate_last_char`

File này cũng in catalog rules và cung cấp `checkPassword()` để nối vào luồng chương trình.

### 6.4. `coverage_problem.py`

Đây là lõi của toàn bộ project.

Nó chứa:

- đọc dữ liệu
- xây dựng coverage sets
- tính coverage
- đóng gói kết quả
- lưu output ra file
- cài đặt toàn bộ solver

Các hàm quan trọng:

- `load_passwords()`
- `build_rule_coverages()`
- `coverage_of_rules()`
- `coverage_counts()`
- `result_payload()`
- `run_solver()`

### 6.5. `algorithms/*.py`

Mỗi file trong `algorithms/` là wrapper cho một solver.

Ví dụ:

- `algorithms/Greedy.py` gọi `solve_greedy()`
- `algorithms/Dynamic_Programming.py` gọi `solve_dp()`
- `algorithms/ILP_PuLP_CBC.py` gọi `solve_ilp_pulp_cbc()`

Các wrapper này thống nhất:

- tên hiển thị trong menu
- tên file output
- chữ ký gọi hàm `solve_max_coverage(k, passwords)`

---

## 7. Luồng chạy đầy đủ của chương trình

### 7.1. Bước 1: khởi động

Chạy:

```bash
python __init__.py
```

### 7.2. Bước 2: in banner và tóm tắt input

Chương trình cho biết:

- file chứa password thật
- file chứa password mutated
- mục tiêu bài toán

### 7.3. Bước 3: xem catalog rules

Người dùng thấy danh sách 20 rules.

Ví dụ:

- `1` `identity_short`
- `2` `identity_medium`
- `6` `append_single_digit`
- `13` `reverse`
- `15` `leet_o0`

### 7.4. Bước 4: nhập `k`

Người dùng chọn số rule phải dùng.

Ví dụ:

- `k = 2`
- `k = 3`
- `k = 10`

### 7.5. Bước 5: chọn thuật toán

Người dùng chọn một solver từ menu.

### 7.6. Bước 6: load dữ liệu

`pwd_checking.py` gọi `load_passwords()` để đọc:

- `real_passwords.txt`
- `mutated_passwords.txt`

### 7.7. Bước 7: dựng coverage sets

`build_rule_coverages()` chạy qua toàn bộ:

- 20 rules
- 500 password thật

Mỗi password thật được transform theo từng rule, rồi so với tập mutated.

### 7.8. Bước 8: solver chọn `k` rules

Mỗi solver dùng chiến lược riêng:

- exact solver tìm nghiệm tối ưu
- heuristic solver tìm nghiệm tốt hoặc gần tốt

### 7.9. Bước 9: ghi kết quả

`result_payload()` đóng gói dữ liệu:

- `selected_rule_ids`
- `selected_rules`
- `covered_set`
- `covered_passwords`
- `coverage_count`

Sau đó `save_answer()` ghi ra file output.

---

## 8. Các solver trong project

### 8.1. Bảng tóm tắt

| Solver | Loại | Ý tưởng chính | Ghi chú |
| --- | --- | --- | --- |
| Greedy | heuristic | Mỗi bước chọn rule có marginal gain lớn nhất | Nhanh, dễ hiểu |
| Randomized Search | heuristic | Lấy mẫu nhiều tập `k` rules ngẫu nhiên | Phụ thuộc số mẫu |
| Hill Climbing | heuristic | Duyệt swap để tăng coverage | Dễ kẹt local optimum |
| Local Search | heuristic | Swap first-improvement từ nghiệm ban đầu | Thực dụng cho bài nhỏ |
| Beam Search | heuristic | Giữ lại `beam_width` trạng thái tốt nhất | Cân bằng giữa rộng và sâu |
| Dynamic Programming | exact | Memoization theo trạng thái tìm kiếm | Chỉ hợp bài nhỏ |
| ILP + PuLP + CBC | exact | Mô hình 0-1 ILP | Dùng solver tối ưu |
| Lagrangian Relaxation | heuristic | Relax ràng buộc bằng penalty | Hữu ích để minh họa tối ưu xấp xỉ |

### 8.2. Greedy

Ý tưởng:

- bắt đầu với tập rỗng
- ở mỗi bước chọn rule thêm được nhiều password mới nhất
- lặp cho tới khi đủ `k`

Ví dụ trên dữ liệu hiện tại:

- rule tốt nhất ở bước đầu là `append_single_digit` với 155 password
- tiếp theo, một lựa chọn tốt là `identity_medium` với 138 password
- với `k = 3`, tập tối ưu hiện tại là:

```text
[2, 4, 6]
= identity_medium, capitalize, append_single_digit
```

Tập này phủ được:

```text
296 / 500 password
```

Greedy trên bộ dữ liệu hiện tại cũng tìm ra đúng coverage này, chỉ khác thứ tự chọn:

```text
[6, 2, 4]
```

Độ phức tạp xấp xỉ:

- dựng coverage: `O(m * n)`
- phần chọn greedy: `O(k * m)` lần xét rule, cộng với chi phí union set

### 8.3. Randomized Search

Ý tưởng:

- sinh ngẫu nhiên nhiều tập `k` rules
- tính coverage của từng tập
- giữ nghiệm tốt nhất

Trong project:

- nếu không truyền số vòng lặp, số lượt thử được tự tính theo kích thước bài toán
- nghiệm greedy được dùng làm baseline ban đầu

Ví dụ:

- nếu `k = 3`, một lần lấy mẫu có thể sinh ra `[4, 8, 20]`
- nếu coverage của tập này thấp hơn `[2, 4, 6]`, nó sẽ bị bỏ

Độ phức tạp xấp xỉ:

- `O(m * n + T * k)` theo số lần lấy mẫu `T`, nếu coi thao tác union set là hằng số tương đối trên dữ liệu nhỏ

### 8.4. Hill Climbing

Ý tưởng:

- khởi đầu từ một nghiệm tốt
- thử các phép đổi `1-swap`
- chỉ chấp nhận bước cải thiện

Trong project:

- khởi tạo từ nghiệm greedy
- dùng `swap_gain()` để ước lượng lợi ích của một swap

Ví dụ:

- nếu đang có tập `[6, 2, 4]`
- thử thay rule 4 bằng rule 12
- nếu coverage giảm, swap bị bỏ

Độ phức tạp xấp xỉ:

- phần xây coverage: `O(m * n)`
- phần local improvement: phụ thuộc số vòng lặp và số swap thử, thường xấp xỉ `O(I * k * m)`

### 8.5. Local Search

Ý tưởng:

- bắt đầu từ một nghiệm ngẫu nhiên hợp lệ
- duyệt lân cận theo kiểu first-improvement
- gặp swap tốt thì nhận ngay

Trong project:

- nghiệm ban đầu được tạo bằng random sample `k` rules
- `coverage_counts()` được dùng để đếm số password được phủ tại trạng thái hiện tại

Ví dụ:

- nếu nghiệm đầu là `[1, 7, 19]`
- solver sẽ thử đổi từng rule này bằng một rule chưa chọn
- khi tìm ra swap có gain dương thì chấp nhận ngay

Độ phức tạp xấp xỉ:

- `O(m * n + I * k * m)`

### 8.6. Beam Search

Ý tưởng:

- mở rộng nhiều trạng thái trung gian
- chỉ giữ lại `beam_width` trạng thái tốt nhất ở mỗi tầng

Trong project:

- beam bắt đầu từ trạng thái rỗng
- ở mỗi độ sâu, solver thử thêm từng rule còn lại
- sau đó sắp xếp theo coverage và cắt xuống `beam_width`

Ví dụ:

- nếu `beam_width = 5`
- solver giữ 5 phương án trung gian tốt nhất thay vì chỉ 1 như greedy

Độ phức tạp xấp xỉ:

- `O(m * n + k * beam_width * m)`

### 8.7. Dynamic Programming

Ý tưởng:

- dùng memoization để tránh tính lại trạng thái đã gặp
- mỗi trạng thái gồm:

```text
start_index
remaining
covered_state
```

Trong project:

- `covered_state` được lưu bằng `frozenset`
- trạng thái được cache bằng `lru_cache`

Ví dụ:

- nếu đã xét các rule đến chỉ số 10 và còn cần chọn 2 rule
- solver sẽ tái sử dụng kết quả nếu cùng trạng thái `covered_state` xuất hiện lại

Đây là solver chính xác, nhưng không gian trạng thái tăng rất nhanh.

Độ phức tạp:

- tốt hơn brute force trong nhiều trường hợp nhỏ
- nhưng vẫn mang bản chất bùng nổ theo trạng thái

### 8.8. ILP + PuLP + CBC

Ý tưởng:

- biến decision `x_i` = có chọn rule `i` hay không
- biến decision `y_j` = password `j` có được phủ hay không
- tối ưu hóa tổng `y_j`

Mô hình trong project:

```text
maximize sum(y_j)
subject to sum(x_i) = k
and y_j <= sum(x_i) for các i có thể phủ password j
```

Ví dụ trực tiếp:

- nếu password `password` có thể được phủ bởi các rule `4, 6, 11, 14, 15, 17`
- thì ràng buộc của `y_password` chỉ liên quan đến các biến `x_4, x_6, x_11, x_14, x_15, x_17`

Ưu điểm:

- đúng với bài toán tối ưu toán học
- trả về nghiệm tối ưu nếu CBC giải được đến tối ưu

### 8.9. Lagrangian Relaxation

Ý tưởng:

- nới lỏng ràng buộc số lượng rule bằng một penalty
- điều chỉnh penalty qua nhiều vòng lặp
- giữ nghiệm khả thi tốt nhất sau khi chiếu lại về miền ràng buộc

Trong project:

- solver xây một nghiệm “relaxed”
- nếu chọn quá nhiều rule thì tăng penalty
- nếu chọn quá ít rule thì giảm penalty

Ví dụ:

- khi `k = 3`, solver có thể tạm thời thử nghiệm một tập lớn hơn hoặc nhỏ hơn
- sau đó dùng `complete_to_k()` hoặc `trim_to_k()` để đưa nghiệm về đúng kích thước `k`

Đây là một heuristic tốt để minh họa tư duy tối ưu có phạt.

---

## 9. Ví dụ chạy thực tế với `k = 3`

Đây là ví dụ dễ nhìn nhất cho Maximum Coverage trong project.

### 9.1. Bài toán

Chọn đúng 3 rules trong 20 rules sao cho số password thật được phủ là lớn nhất.

### 9.2. Kết quả tối ưu trên dữ liệu hiện tại

Brute force cho `k = 3` trả về:

```text
[2, 4, 6]
```

Tương ứng:

- `identity_medium`
- `capitalize`
- `append_single_digit`

Coverage:

```text
296 / 500
```

### 9.3. Vì sao ví dụ này quan trọng

Nó cho thấy ba điều:

- rule mạnh nhất đơn lẻ chưa chắc đã đủ
- cần xét overlap giữa các tập phủ
- cách chọn bộ 3 rules tốt nhất không thể đoán chỉ bằng nhìn từng rule riêng lẻ

### 9.4. So sánh với greedy

Greedy trên dữ liệu hiện tại cũng đạt cùng coverage:

```text
[6, 2, 4]
```

Điều này không phải lúc nào cũng xảy ra, nhưng đây là một ví dụ đẹp để minh họa rằng:

- greedy có thể rất tốt trên dữ liệu thực
- nhưng ta vẫn cần brute force / ILP để biết nghiệm tối ưu thực sự

---

## 10. Định dạng kết quả và file output

### 10.1. `result_payload()`

Kết quả sau khi giải được đóng gói theo cùng một định dạng.

Các trường chính:

- `method`
- `k`
- `selected_rule_ids`
- `selected_rules`
- `covered_set`
- `covered_indices`
- `covered_passwords`
- `coverage_count`
- `total_passwords`
- `mutated_passwords`

### 10.2. `save_answer()`

Kết quả được lưu ra file output riêng.

Ví dụ tên file:

- `output_greedy_k3.txt`
- `output_randomized_k4.txt`
- `output_hill_k4.txt`
- `output_local_k4.txt`
- `output_beam_k4.txt`
- `output_dp_k7.txt`
- `output_ILP_PuLP_CBC_k10.txt`
- `output_lagrangian_k10.txt`

### 10.3. Nội dung file output

File output thường có:

- tên phương pháp
- giá trị `k`
- số password thật và mutated
- các rules được chọn
- danh sách password được phủ
- tỷ lệ coverage

---

## 11. Độ phức tạp và cách đọc dự án

### 11.1. Chi phí chung

Mọi solver đều dựa trên cùng một bước tiền xử lý:

- duyệt 20 rules
- duyệt 500 password thật
- dựng tập phủ cho từng rule

Phần này xấp xỉ `O(m * n)`.

### 11.2. Nơi tốn nhất trong project

Chi phí chủ yếu đến từ:

- tính coverage ban đầu
- lặp qua nhiều trạng thái khi tìm nghiệm
- union / difference trên các tập phủ

### 11.3. Cách đọc code hiệu quả

Nếu muốn hiểu nhanh project, nên đọc theo thứ tự:

1. `rules.py`
2. `coverage_problem.py`
3. `__init__.py`
4. `pwd_checking.py`
5. `algorithms/*.py`

---

## 12. Ghi chú quan trọng

- Project hiện tại không dùng bitmask số nguyên để lưu tập phủ
- Mọi solver đều dùng `set`/`frozenset`
- `rules.py` là nơi quyết định “rule nào có thể tạo ra candidate gì”
- `coverage_problem.py` là nơi quyết định “tập nào được phủ bởi rule nào”
- `algorithms/` chỉ là lớp wrapper để gọi solver tương ứng

Nếu muốn mở rộng project, hướng tự nhiên nhất là:

- thêm rule mới vào `rules.py`
- thêm solver mới vào `coverage_problem.py`
- thêm wrapper tương ứng trong `algorithms/`

---

## 13. Kết luận

Project này là một ví dụ khá sạch cho cách biến một bài toán chuỗi thực tế thành một bài toán tối ưu tổ hợp.

Điểm mạnh của cách triển khai hiện tại là:

- mô hình rõ ràng
- code dễ đọc hơn bitmask
- có cả exact solver lẫn heuristic solver
- có thể dùng để minh họa độ phức tạp, NP-Hard, và trade-off giữa tốc độ với chất lượng nghiệm

Nếu nhìn từ góc độ học thuật, đây là một bài toán Maximum Coverage rất phù hợp để học:

- cách mô hình hóa
- cách dựng tập phủ
- cách so sánh exact vs heuristic
- cách phân tích overlap giữa các tập con

