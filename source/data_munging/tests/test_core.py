from .context import world

import unittest

class WorldTest(unittest.TestCase):
    def setUp(self):
        self.alpha = world.Component('alpha', ('wheat', 'oil', 'coal', 'money'), ('a', 'b'), ('c', 'd'))
        self.bravo = world.Component('bravo', ('iron', 'steel', 'money'), ('a', 'b'), ('c', 'd'))
        self.agent = world.Agent('First')
        
    def test_agent_add(self):
        self.agent.add(self.alpha)
        self.agent.add(self.bravo)
        value = self.agent.parts[self.alpha.identifier]
        assert value == self.alpha
        value = self.agent.parts[self.bravo.identifier]
        assert value == self.bravo
        
if __name__ == '__main__':
    unittest.main()

