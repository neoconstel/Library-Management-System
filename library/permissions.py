import rules


# define predicates
@rules.predicate
def is_order_creator(user, order):
    return order.student.user == user


# create django permissions (would be implemented in model meta class instead)
# rules.add_perm('library.change_order', is_order_creator)
# rules.add_perm('library.delete_order', is_order_creator)

