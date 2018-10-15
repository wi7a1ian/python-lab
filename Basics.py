# Beautiful is better than ugly
#-----------------------------------------------------------------------
halve_evens_only = lambda nums: map(lambda i: i/2, filter(lambda i: not i%2, nums))
def halve_evens_only(nums):
  """ easier to read """
  return [i/2 for i in nums if not i % 2]

# Swaping two variables
a, b = 1, 2
a, b = b, a
print(a, b)

# The step argument in slice operators.
a = [1,2,3,4,5]
print(a[::2])

# The special case x[::-1] is a useful idiom for ‘x reversed’.
print(a[::-1])
# Do keep in mind x.reverse() reverses the list in place.

# Don’t use mutables as defaults
def function(x, l=[]):          # Don't do this
  pass
def function(x, l=None):        # Way better
  if l is None:
    l = []
  pass

# Use iteritems rather than items
s = "test"
seq = [1,2,3]
print(isinstance(s, str), isinstance(seq, (list, tuple)))

# Conditional Assignments
a = 3 if (b == 1) else 2
