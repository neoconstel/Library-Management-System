import rules


# define predicates
@rules.predicate
def is_order_creator(user, order):
    return order.student.user == user

@rules.predicate
def is_with_book(user, book):
    return user.student.order_set.filter(book=book).exists()

is_staff_or_with_book = rules.is_staff|is_with_book


# create django permissions (would be implemented in model meta class instead)
# rules.add_perm('library.change_order', is_order_creator)
# rules.add_perm('library.delete_order', is_order_creator)

