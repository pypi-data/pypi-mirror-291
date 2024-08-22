#!/usr/bin/env python
import unittest
from Clict import Clict


class TestClict(unittest.TestCase):


	def test_set_get(s):
		a = Clict(a=1, b=2)
		c = Clict()
		j = Clict()
		c['a'] = 1
		c.b = 2
		j.d.missing
		s.assertEqual(c, a)
		s.assertEqual(c['a'], 1)
		s.assertEqual(c.b, 2)
		s.assertEqual(c.a, 1)
		s.assertEqual(c['b'], 2)

		s.assertIsInstance(j.d.missing, Clict)
		s.assertIn('a', c)
		s.assertNotIn('d', c)
		s.assertListEqual(list(c.keys()), ['a', 'b'])
		s.assertDictEqual(c.items(), {'a': 1, 'b': 2})
		s.assertListEqual(c.values(), [1, 2])

	def test_set_parent(s):
		c = Clict()
		c.d.asplit.child='findme'
		c.d.bsplit.child='fromhere'
		# localparent=c.d.__setparent__('iamparent')
		s.assertEqual(c.d.bsplit.__getparent__()().asplit.child,'findme')

	# def test_str(s):
	# 	c = Clict(a=1, b=2)
	# 	s.assertIsInstance(str(c), str)
	#


	def test_fromdict(s):
		c = Clict()
		c.__fromdict__({'a': {'b': 2}})
		s.assertIsInstance(c['a'], Clict)
		s.assertEqual(c['a']['b'], 2)
	def test_fromlist(s):
		c = Clict()
		c.__fromlist__(['a','b'])
		s.assertEqual(c[0], 'a')
		s.assertEqual(c[1], 'b')
		c=Clict(['a','b'])
		s.assertEqual(c[0], 'a')
		s.assertEqual(c[1], 'b')
		s.assertEqual(c._1, 'b')
		c=Clict(mylist=['a','b'])
		s.assertEqual(c.mylist[0], 'a')
		c.mylist[2]='c'
		s.assertEqual(c.mylist._2, 'c')
	def test_printtree(s):
		c=Clict(['a','b'],g=['d',{'e':'f'}])
		c.p.q.r.s.t.u.v.w.x.y='test'
		c.p.q.r.s.t.u.v.w.x.a= print
		c.p.r.s.z=['i' for i in range(90)]
		print(c)
		print(repr(c))
		print([*c])


if __name__ == '__main__':
	unittest.main()
