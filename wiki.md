# Wiki: Password Checking Maximum Coverage

## Mục lục

- [Phần 1. Lý thuyết nền tảng](#phần-1-lý-thuyết-nền-tảng)
  - [1. Bài toán NP là gì](#1-bài-toán-np-là-gì)
  - [2. NP-Hard là gì](#2-np-hard-là-gì)
  - [3. Maximum Coverage là gì](#3-maximum-coverage-là-gì)
  - [4. Thuật toán là gì](#4-thuật-toán-là-gì)
  - [5. Lý thuyết từng thuật toán trong `algorithms/`](#5-lý-thuyết-từng-thuật-toán-trong-algorithms)
- [Phần 2. Cách hoạt động của dự án](#phần-2-cách-hoạt-động-của-dự-án)
  - [1. Mục tiêu triển khai](#1-mục-tiêu-triển-khai)
  - [2. Chức năng của từng file](#2-chức-năng-của-từng-file)
  - [3. `rules.py` gồm những rules gì](#3-rulespy-gồm-những-rules-gì)
  - [4. Maximum Coverage hoạt động như thế nào trong dự án](#4-maximum-coverage-hoạt-động-như-thế-nào-trong-dự-án)
  - [5. Luồng chạy đầy đủ của chương trình](#5-luồng-chạy-đầy-đủ-của-chương-trình)

## Phần 1. Lý thuyết nền tảng

### 1. Bài toán NP là gì

NP là viết tắt của **Nondeterministic Polynomial time**.

Một bài toán quyết định được gọi là thuộc lớp NP nếu:

- một lời giải ứng viên của bài toán có thể được kiểm tra trong thời gian đa thức
- tức là, nếu ai đó đưa ra một nghiệm, ta có thể xác minh nghiệm đó đúng hay sai tương đối nhanh

Điều cần nhớ:

- NP không có nghĩa là “khó”
- NP có nghĩa là “kiểm tra được nhanh”
- nhiều bài toán trong NP vẫn có thể rất khó để tìm lời giải tối ưu

Ví dụ:

- bài toán kiểm tra một số có phải là nghiệm của một phương trình hay không
- bài toán tìm tập con thỏa điều kiện nào đó

### 2. NP-Hard là gì

Một bài toán được gọi là **NP-Hard** nếu nó khó ít nhất bằng mọi bài toán trong NP.

Nói trực quan:

- nếu bạn giải được một bài toán NP-Hard thật nhanh
- thì bạn có thể kéo theo việc giải nhanh rất nhiều bài toán NP khác

Điều quan trọng:

- NP-Hard không nhất thiết phải thuộc NP
- NP-Hard là mức độ khó của bài toán tối ưu hoặc bài toán tổng quát

Ví dụ các bài toán NP-Hard quen thuộc:

- Travelling Salesman Problem
- Knapsack
- Set Cover
- Maximum Coverage

### 3. Maximum Coverage là gì

Maximum Coverage là bài toán:

- có một tập vũ trụ `U`
- có nhiều tập con `S1, S2, ..., Sm`
- được phép chọn tối đa `k` tập
- mục tiêu là làm cho số phần tử trong hợp của các tập được chọn là lớn nhất

Công thức:

```text
maximize |S1 ∪ S2 ∪ ... ∪ Sk|
```

với ràng buộc:

```text
chỉ được chọn tối đa k tập
```

Đây là bài toán tối ưu tổ hợp vì:

- số lượng cách chọn tập tăng rất nhanh khi số tập tăng
- thử hết tất cả tổ hợp thường không khả thi với dữ liệu lớn

#### Ví dụ

Giả sử:

```text
U = {1,2,3,4,5,6,7,8}
S1 = {1,2,3}
S2 = {3,4,5}
S3 = {5,6,7}
S4 = {7,8}
```

Nếu chọn `k = 2`:

- `S1 ∪ S2 = {1,2,3,4,5}` → phủ 5 phần tử
- `S1 ∪ S4 = {1,2,3,7,8}` → phủ 5 phần tử
- `S2 ∪ S3 = {3,4,5,6,7}` → phủ 5 phần tử
- `S3 ∪ S4 = {5,6,7,8}` → phủ 4 phần tử

Lời giải tốt có thể là một trong các cặp phủ được 5 phần tử.

### 4. Thuật toán là gì

Thuật toán là một chuỗi các bước rõ ràng để giải một bài toán.

Trong bối cảnh project này, thuật toán là cách để:

- chọn rules nào
- chọn theo tiêu chí gì
- đạt được coverage lớn nhất hoặc gần lớn nhất

Khi bài toán là NP-Hard, thuật toán thường được chia thành 3 kiểu:

- thuật toán chính xác
- thuật toán xấp xỉ
- thuật toán tối ưu hóa trên không gian trạng thái

### 5. Lý thuyết từng thuật toán trong `algorithms/`

#### 5.1. Brute Force

Ý tưởng:

- thử mọi tổ hợp gồm đúng `k` rules
- tính coverage của từng tổ hợp
- lấy tổ hợp có coverage lớn nhất

Tính chất:

- chính xác tuyệt đối
- chi phí tăng rất nhanh theo số lượng rules

Độ phức tạp:

- số tổ hợp là `C(m, k)` với `m` là số rules
- với mỗi tổ hợp, cần tính hợp của các tập

Ví dụ:

- có 20 rules, chọn 5
- số tổ hợp là `C(20,5) = 15504`

#### 5.2. Greedy

Ý tưởng:

- ở mỗi bước, chọn rule đem lại nhiều phần tử mới được phủ nhất
- tiếp tục cho đến khi đủ `k` rules

Tính chất:

- rất phổ biến với Maximum Coverage
- nhanh hơn brute force rất nhiều
- không luôn cho nghiệm tối ưu tuyệt đối

Ví dụ:

- ban đầu chọn rule phủ 100 phần tử
- ở bước sau, chọn rule phủ thêm 40 phần tử mới thay vì rule khác phủ thêm 35

#### 5.3. ILP_PuLP_CBC

Ý tưởng:

- xây dựng mô hình 0-1 Integer Linear Programming cho Maximum Coverage
- biến quyết định nhị phân `x_i` cho biết có chọn rule `i` hay không
- biến quyết định nhị phân `y_j` cho biết password `j` có được phủ hay không
- giải bằng PuLP và CBC Solver

Tính chất:

- vẫn là lời giải chính xác
- đúng với cách mô hình toán được viết trong lý thuyết tối ưu
- dùng bitmask chỉ để dựng hệ số `a_ij` và tính coverage sau khi có nghiệm

Ví dụ:

- nếu rule `i` được chọn thì `x_i = 1`
- nếu password thứ 3 được phủ thì `y_3 = 1`
- các ràng buộc đảm bảo một password chỉ được tính là phủ khi ít nhất một rule đã chọn sinh ra nó

#### 5.4. Dynamic Programming

Ý tưởng:

- chia bài toán thành các trạng thái nhỏ hơn
- dùng memoization để lưu kết quả trung gian
- tránh tính lại cùng một trạng thái nhiều lần

Tính chất:

- chính xác
- hiệu quả hơn brute force trong các trường hợp có trạng thái lặp

Ví dụ:

- nếu đã xét từ rule thứ `i` với `remaining = 2`
- kết quả của trạng thái đó có thể được dùng lại nhiều lần khi truy hồi

#### 5.5. Bitmask trong project

Bitmask là cách biểu diễn tập con bằng số nhị phân.

Ví dụ:

- bit `1` tại vị trí `i` nghĩa là phần tử thứ `i` được chọn hoặc được phủ

Lợi ích:

- union tập chỉ còn là phép `OR`
- kiểm tra số phần tử phủ được có thể dùng `bit_count()`

---

## Phần 2. Cách hoạt động của dự án

### 1. Mục tiêu triển khai

Project này không đơn thuần là kiểm tra password.

Mục tiêu chính là:

- mô hình hóa bài toán password matching thành Maximum Coverage
- so sánh độ phức tạp giữa các chiến lược giải khác nhau
- quan sát cách một bài toán NP-Hard được xử lý trong thực tế

Nói cách khác:

- `real_passwords.txt` là tập vũ trụ cần được phủ
- `mutated_passwords.txt` là tập so khớp đích
- mỗi rule là một phép biến đổi password áp lên password thật
- chọn `k` rules sao cho số password thật sinh ra biến thể thuộc tập mutated là lớn nhất

### 2. Chức năng của từng file

#### `__init__.py`

Đây là file chạy chính.

Chức năng:

- hiển thị banner
- in danh sách rules
- yêu cầu người dùng nhập số lượng rules `k`
- cho phép chọn thuật toán
- điều phối luồng chạy giữa menu rules và menu thuật toán

#### `pwd_checking.py`

Đây là menu chọn thuật toán.

Chức năng:

- in menu Brute Force / Greedy / ILP_PuLP_CBC / Dynamic Programming
- nhận lựa chọn từ người dùng
- gọi đúng module thuật toán tương ứng
- xử lý các phím điều hướng như `0`, `-1`

#### `rules.py`

Đây là nơi định nghĩa toàn bộ rules và menu rules.

Chức năng:

- chứa 20 rule mutation
- in catalog các rule
- hỗ trợ load dữ liệu đầu vào thông qua module thuật toán
- điều phối call sang solver qua `checkPassword()`

#### `coverage_problem.py`

Đây là file lõi của bài toán.

Chức năng:

- đọc file password
- chuyển rules thành bitmask
- tính coverage
- định dạng kết quả
- lưu output ra file
- cài đặt 4 solver:
  - brute force
  - greedy
  - ILP_PuLP_CBC
  - dynamic programming

#### `algorithms/Brute_Force.py`

Wrapper cho giải pháp brute force.

Chức năng:

- gọi `solve_bruteforce()`
- đặt tên output là `output_brute`

#### `algorithms/Greedy.py`

Wrapper cho giải pháp greedy.

Chức năng:

- gọi `solve_greedy()`
- đặt tên output là `output_greedy`

#### `algorithms/ILP_PuLP_CBC.py`

Wrapper cho giải pháp ILP exact dùng PuLP + CBC.

Chức năng:

- gọi `solve_ilp_pulp_cbc()`
- đặt tên output là `output_ILP_PuLP_CBC`

#### `algorithms/Dynamic_Programming.py`

Wrapper cho giải pháp quy hoạch động.

Chức năng:

- gọi `solve_dp()`
- đặt tên output là `output_dp`

#### `real_passwords.txt`

- chứa danh sách password thật
- là tập cần được phủ trong bài toán

#### `mutated_passwords.txt`

- chứa danh sách password đã biến đổi hoặc password đầu vào để áp dụng rules

#### `output_*.txt`

- chứa kết quả sau mỗi lần chạy solver
- mỗi file tương ứng với một thuật toán và một giá trị `k`

#### `README.md`

- tài liệu giới thiệu ngắn gọn
- hướng dẫn sử dụng ở mức tổng quan

#### `wiki.md`

- tài liệu lý thuyết và mô tả hệ thống chi tiết này

### 3. `rules.py` gồm những rules gì

Project hiện có 20 rules:

1. `identity`
2. `capitalize`
3. `uppercase_all`
4. `append_1`
5. `append_12`
6. `append_123`
7. `append_year`
8. `prepend_1`
9. `prepend_123`
10. `reverse`
11. `leet_a4`
12. `leet_o0`
13. `leet_e3`
14. `leet_s$`
15. `mixed_leet`
16. `keyboard_walk`
17. `keyboard_walk_number`
18. `numeric_sequence`
19. `repeated_digit`
20. `duplicate_last_char`

#### Ý nghĩa từng rule

- `identity`: giữ nguyên chuỗi
- `capitalize`: viết hoa ký tự đầu
- `uppercase_all`: chuyển toàn bộ thành chữ hoa
- `append_1`: thêm `1` vào cuối
- `append_12`: thêm `12` vào cuối
- `append_123`: thêm `123` vào cuối
- `append_year`: thêm một năm từ 1990 đến 2030
- `prepend_1`: thêm `1` vào đầu
- `prepend_123`: thêm `123` vào đầu
- `reverse`: đảo ngược chuỗi
- `leet_a4`: thay `a` hoặc `A` bằng `4`
- `leet_o0`: thay `o` hoặc `O` bằng `0`
- `leet_e3`: thay `e` hoặc `E` bằng `3`
- `leet_s$`: thay `s` hoặc `S` bằng `$`
- `mixed_leet`: kết hợp nhiều kiểu leetspeak
- `keyboard_walk`: nối thêm `qwerty`
- `keyboard_walk_number`: nối thêm `qwerty123`
- `numeric_sequence`: nối thêm `123456`
- `repeated_digit`: nối thêm một chuỗi gồm cùng một số lặp lại 3 lần
- `duplicate_last_char`: lặp lại ký tự cuối cùng

### 4. Maximum Coverage hoạt động như thế nào trong dự án

Trong project này, bài toán Maximum Coverage được hiểu theo cách sau:

- `U` là tập toàn bộ password thật
- mỗi rule tạo ra một tập các password thật mà nó có thể sinh ra biến thể nằm trong tập mutated
- hợp của các tập do rules tạo ra chính là số password thật được cover
- mục tiêu là chọn tối đa `k` rules để cover được nhiều password thật nhất

#### Cách xây dựng tập phủ

1. Đọc toàn bộ password thật
2. Đọc toàn bộ password mutated
3. Với mỗi rule:
   - áp dụng rule lên từng password thật
   - sinh ra các candidate password
   - nếu candidate xuất hiện trong tập mutated thì password đó được tính là phủ
4. Mỗi rule tương ứng với một tập con các password thật

#### Cách tính coverage

- nếu một password thật được ít nhất một rule phủ, nó được tính vào kết quả
- nếu nhiều rule cùng phủ một password, password đó vẫn chỉ được tính một lần
- mục tiêu là hợp các tập phủ lớn nhất có thể với số rule giới hạn là `k`

#### Vai trò của `k`

- `k` là số rules tối đa được phép chọn
- nếu `k` nhỏ, bài toán khó hơn vì phải chọn rất kỹ
- nếu `k` lớn, coverage thường tăng nhưng cũng tốn thời gian hơn khi tìm tối ưu

### 5. Luồng chạy đầy đủ của chương trình

#### Bước 1: Khởi động

Chạy:

```bash
python __init__.py
```

#### Bước 2: Hiển thị banner

Chương trình in banner giới thiệu project.

#### Bước 3: Hiển thị danh sách rules

Người dùng nhìn thấy catalog các rules mutation.

#### Bước 4: Nhập `k`

Người dùng nhập số lượng rules cần chọn.

Các lựa chọn thường gặp:

- nhập `1` đến `20`
- nhập `0` hoặc `e` để thoát

#### Bước 5: Chọn thuật toán

Menu thuật toán cho phép chọn:

- `1` Brute Force
- `2` Greedy
- `3` ILP_PuLP_CBC
- `4` Dynamic Programming
- `0` quay lại menu trước
- `-1` hoặc `e` thoát chương trình

#### Bước 6: Load dữ liệu

`coverage_problem.py` đọc:

- `real_passwords.txt`
- `mutated_passwords.txt`

#### Bước 7: Tính coverage

Mỗi solver:

- dựng bitmask cho từng rule
- chọn `k` rules theo chiến lược riêng
- tính số password thật được phủ

#### Bước 8: Xuất kết quả

Kết quả được:

- in ra màn hình
- lưu vào file output tương ứng

#### Bước 9: Lặp lại hoặc thoát

Người dùng có thể:

- quay lại chọn `k`
- đổi thuật toán
- thoát chương trình

---

## Gợi ý đọc thêm

Nếu bạn muốn dùng wiki này cho báo cáo, nên viết thêm:

- độ phức tạp Big-O của từng thuật toán
- ví dụ cụ thể với bảng tập hợp
- nhận xét vì sao greedy là xấp xỉ, còn brute force/DP là exact
- kết luận về NP-Hard trong project
