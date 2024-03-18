import unittest


def suite():
    suite = unittest.TestSuite()

    # ---- test mail assistant ---
    from mail_assistant import TestMailAssistant
    suite.addTest(TestMailAssistant("test_parse_mail"))
    suite.addTest(TestMailAssistant("test_gen_mail"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
