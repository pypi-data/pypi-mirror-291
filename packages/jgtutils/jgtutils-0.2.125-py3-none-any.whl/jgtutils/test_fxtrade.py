import unittest
from unittest.mock import patch, MagicMock
from FXTransact import FXTrade

class TestFXTrade(unittest.TestCase):
    @patch('FXTransact.FXTrade.fromid')
    def test_fromid_valid_trade_id(self, mock_fromid):
        trade_id = 123
        mock_trade = MagicMock(spec=FXTrade)
        mock_trade.trade_id = trade_id
        mock_fromid.return_value = mock_trade

        trade = FXTrade.fromid(trade_id)
        self.assertIsInstance(trade, FXTrade)
        self.assertEqual(trade.trade_id, trade_id)

    @patch('FXTransact.FXTrade.fromid')
    def test_fromid_invalid_trade_id(self, mock_fromid):
        trade_id = -1
        mock_fromid.return_value = None

        trade = FXTrade.fromid(trade_id)
        self.assertIsNone(trade)
        
    

if __name__ == '__main__':
    unittest.main()