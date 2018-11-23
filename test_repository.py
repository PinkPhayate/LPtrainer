from line_botr import repository
from line_botr.training import Training
def test_get_training_menu():
    uid = "Ud2a90a4a1af6999f9f9ceaa10f63ba6b"
    data = repository.get_training_menu(uid)
    data = [Training(x[0]) for x in data]
    print(data)

def test_get_records():
    uid = "5bc2c43f2f5c47a0a73e524a771ff5b4"
    data = repository.get_records(uid)
    lst = [Training(t[0][0]) for t in data]
    print(lst)
    # data = [" ".join(map(str, d)) for d in data]
    # data_str = "\n".join(data)
# test_get_training_menu()
test_get_records()
