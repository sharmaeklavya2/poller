# coding: utf-8
from __future__ import print_function
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User

import os
import json
import six

from main.models import Question, Option, Choice
from main.models import choose, unchoose

from lib import populate
from lib.exceptions import BadDataError
from lib.response import get_response_str
from lib.testing import encode_data, do_test_login, do_test_basic_auth, do_logout, do_test_register, do_test_vote
from lib.textutil import force_text, force_str

from six import text_type

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_FILE = os.path.join(BASE_DIR, "lib", "test_data.json")
TEST_QLIST = json.load(open(TEST_DATA_FILE))
FORM_CONTENT_TYPE = 'application/x-www-form-urlencoded'

s_fav_fruit = "मनपसंद फल?"
s_anaar = "अनार"
s_lichi = "लीची"
s_chikoo = "चीकू"

class TestTesting(TestCase):
    def test_encode_empty_form1(self):
        self.assertEqual(encode_data(None), {})
        self.assertEqual(encode_data(""), "")
        self.assertEqual(encode_data([]), [])
        self.assertEqual(encode_data({}), {})

    def test_encode_empty_form2(self):
        self.assertEqual(encode_data(None, FORM_CONTENT_TYPE), "")
        self.assertEqual(encode_data({}, FORM_CONTENT_TYPE), "")
        self.assertEqual(encode_data("", FORM_CONTENT_TYPE), "")
        with self.assertRaises(BadDataError):
            encode_data([], FORM_CONTENT_TYPE)

    def test_encode_empty_json(self):
        with self.assertRaises(BadDataError):
            encode_data(None, "application/json")
        self.assertEqual(encode_data("", "application/json"), '""')
        self.assertEqual(encode_data(0, "application/json"), '0')
        self.assertEqual(encode_data([], "application/json"), '[]')
        self.assertEqual(encode_data({}, "application/json"), '{}')

    def test_encode_dict_form1(self):
        d1 = {"username": "user1", "password": "pass1"}
        self.assertEqual(encode_data(d1), d1)
        d2 = {"values": ["a", "b", "c"]}
        self.assertEqual(encode_data(d2), d2)
        d3 = {"values": [1, 2, 3]}
        self.assertEqual(encode_data(d3), d3)
        d4 = {"value": 0}
        self.assertEqual(encode_data(d4), d4)
        d5 = {"values": [1, 2, 3], "username": "user1"}
        self.assertEqual(encode_data(d5), d5)
        d6 = {"username": s_chikoo, "password": "pass1"}
        self.assertEqual(encode_data(d6), d6)

    def test_encode_dict_form2(self):
        d1 = {"username": "user1", "password": "pass1"}
        res1 = ('username=user1&password=pass1', 'password=pass1&username=user1')
        self.assertIn(encode_data(d1, FORM_CONTENT_TYPE), res1)
        d2 = {"values": ["a", "b"]}
        res2 = 'values=a&values=b'
        self.assertEqual(encode_data(d2, FORM_CONTENT_TYPE), res2)
        d3 = {"values": [1, 2]}
        res3 = 'values=1&values=2'
        self.assertEqual(encode_data(d3, FORM_CONTENT_TYPE), res3)
        d4 = {"value": 0}
        res4 = 'value=0'
        self.assertEqual(encode_data(d4, FORM_CONTENT_TYPE), res4)
        d5 = {"values": [1, 2], "username": "user1"}
        res5 = ('username=user1&values=1&values=2', 'values=1&values=2&username=user1')
        self.assertIn(encode_data(d5, FORM_CONTENT_TYPE), res5)
        d6 = {"username": s_chikoo, "password": "pass1"}
        res6 = ('username=%E0%A4%9A%E0%A5%80%E0%A4%95%E0%A5%82&password=pass1',
                'password=pass1&username=%E0%A4%9A%E0%A5%80%E0%A4%95%E0%A5%82')
        self.assertIn(encode_data(d6, FORM_CONTENT_TYPE), res6)

    def test_encode_dict_json(self):
        d1 = {"username": "user1", "password": "pass1"}
        res1 = force_text(json.dumps(d1))
        self.assertEqual(encode_data(d1, "application/json"), res1)
        d2 = {"username": s_chikoo, "password": "pass1"}
        res2 = force_text(json.dumps(d2))
        self.assertEqual(encode_data(d2, "application/json"), res2)

    def test_encode_list_form1(self):
        l1 = ['a', 'b']
        self.assertEqual(encode_data(l1), l1)
        l2 = [s_anaar, s_chikoo]
        self.assertEqual(encode_data(l2), l2)

    def test_encode_list_form2(self):
        l1 = ['a', 'b']
        with self.assertRaises(BadDataError):
            encode_data(l1, FORM_CONTENT_TYPE)
        l2 = [s_anaar, s_chikoo]
        with self.assertRaises(BadDataError):
            encode_data(l2, FORM_CONTENT_TYPE)

    def test_encode_list_json(self):
        l1 = ['a', 'b']
        res1 = force_text(json.dumps(l1))
        self.assertEqual(encode_data(l1, "application/json"), res1)
        l2 = [1, 2]
        res2 = force_text(json.dumps(l2))
        self.assertEqual(encode_data(l2, "application/json"), res2)
        l3 = [s_anaar, s_chikoo]
        res3 = force_text(json.dumps(l3))
        self.assertEqual(encode_data(l3, "application/json"), res3)

class TestModels(TestCase):
    def test_question_str(self):
        """Checks Question.__str__"""
        q1 = Question(title="OS", text="Favorite OS?")
        self.assertEqual(text_type(q1), "OS")
        q2 = Question(text="Favorite food?")
        self.assertEqual(text_type(q2), "Favorite food?")
        q3 = Question(text=s_fav_fruit)
        self.assertEqual(text_type(q3), s_fav_fruit)
        self.assertEqual(str(q3), force_str(s_fav_fruit))


    def test_question_to_dict(self):
        """Checks Question.to_dict"""
        q = Question(title="OS", text="Favorite OS?", multivote=False, locked=False, show_count=True)
        q.save()
        o1 = Option(text="Linux", question=q)
        o2 = Option(text="Windows", question=q)
        o3 = Option(text="Mac", question=q)
        o4 = Option(text=s_chikoo, question=q)
        o1.save()
        o2.save()
        o3.save()
        o4.save()

        qdict = {
            "title": "OS",
            "text": "Favorite OS?",
            "multivote": False,
            "locked": False,
            "show_count": True,
            "options": ["Linux", "Windows", "Mac", s_chikoo],
        }

        self.assertEqual(q.to_dict(), qdict)

class TestChoosing(TestCase):
    def setUp(self):
        User.objects.create_user('user1')
        User.objects.create_user('user2')
        populate.add_qlist(TEST_QLIST)

    def test_empty(self):
        choices = Choice.objects.all()
        self.assertEqual(choices.count(), 0)
        for option in Option.objects.all():
            self.assertEqual(option.vote_count(), 0)

    def test_simple_choose(self):
        u1 = User.objects.get(username='user1')
        u2 = User.objects.get(username='user2')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")
        atom = Option.objects.get(question=qed, text="Atom")

        choose(u1, vim)
        choose(u1, linux)
        choose(u2, atom)
        choose(u2, linux)

        ed_choices1 = Choice.objects.filter(user=u1, option__question=qed)
        ed_choices2 = Choice.objects.filter(user=u2, option__question=qed)
        os_choices1 = Choice.objects.filter(user=u1, option__question=qos)
        os_choices2 = Choice.objects.filter(user=u2, option__question=qos)

        self.assertEqual(ed_choices1.count(), 1)
        self.assertEqual(ed_choices2.count(), 1)
        self.assertEqual(os_choices1.count(), 1)
        self.assertEqual(os_choices2.count(), 1)
        self.assertEqual(ed_choices1.first().option_id, vim.id)
        self.assertEqual(ed_choices2.first().option_id, atom.id)
        self.assertEqual(os_choices1.first().option_id, linux.id)
        self.assertEqual(os_choices2.first().option_id, linux.id)

        self.assertEqual(vim.vote_count(), 1)
        self.assertEqual(atom.vote_count(), 1)
        self.assertEqual(linux.vote_count(), 2)

    def test_separate_choose(self):
        user = User.objects.get(username='user1')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")
        atom = Option.objects.get(question=qed, text="Atom")
        windows = Option.objects.get(question=qos, text="Windows")

        self.assertEqual(choose(user, atom), True)
        self.assertEqual(choose(user, windows), True)
        ed_choices1 = Choice.objects.filter(user=user, option__question=qed)
        os_choices1 = Choice.objects.filter(user=user, option__question=qos)
        self.assertEqual(ed_choices1.count(), 1)
        self.assertEqual(os_choices1.count(), 1)
        self.assertEqual(ed_choices1[0].option_id, atom.id)
        self.assertEqual(os_choices1[0].option_id, windows.id)

        self.assertEqual(choose(user, vim), True)
        self.assertEqual(choose(user, linux), True)
        ed_choices2 = Choice.objects.filter(user=user, option__question=qed).order_by('id')
        os_choices2 = Choice.objects.filter(user=user, option__question=qos).order_by('id')
        self.assertEqual(ed_choices2.count(), 2)
        self.assertEqual(os_choices2.count(), 1)
        self.assertEqual(ed_choices2[0].option_id, atom.id)
        self.assertEqual(ed_choices2[1].option_id, vim.id)
        self.assertEqual(os_choices2[0].option_id, linux.id)

    def test_same_choose(self):
        user = User.objects.get(username='user1')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")

        self.assertEqual(choose(user, vim), True)
        self.assertEqual(choose(user, linux), True)
        ed_choices1 = Choice.objects.filter(user=user, option__question=qed)
        os_choices1 = Choice.objects.filter(user=user, option__question=qos)
        self.assertEqual(ed_choices1.count(), 1)
        self.assertEqual(os_choices1.count(), 1)
        self.assertEqual(ed_choices1.first().option_id, vim.id)
        self.assertEqual(os_choices1.first().option_id, linux.id)

        self.assertEqual(choose(user, vim), False)
        self.assertEqual(choose(user, linux), False)
        ed_choices2 = Choice.objects.filter(user=user, option__question=qed)
        os_choices2 = Choice.objects.filter(user=user, option__question=qos)
        self.assertEqual(ed_choices2.count(), 1)
        self.assertEqual(os_choices2.count(), 1)
        self.assertEqual(ed_choices2.first().option_id, vim.id)
        self.assertEqual(os_choices2.first().option_id, linux.id)

    def test_unchoose_empty(self):
        user = User.objects.get(username='user1')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")

        self.assertEqual(unchoose(user, vim), False)
        self.assertEqual(unchoose(user, linux), False)
        self.assertEqual(Choice.objects.filter(user=user, option__question=qed).count(), 0)
        self.assertEqual(Choice.objects.filter(user=user, option__question=qos).count(), 0)

        self.assertEqual(vim.vote_count(), 0)
        self.assertEqual(linux.vote_count(), 0)

    def test_unchoose_chosen(self):
        u1 = User.objects.get(username='user1')
        u2 = User.objects.get(username='user2')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")

        self.assertEqual(choose(u1, vim), True)
        self.assertEqual(choose(u1, linux), True)
        self.assertEqual(choose(u2, vim), True)
        self.assertEqual(choose(u2, linux), True)
        self.assertEqual(unchoose(u1, vim), True)
        self.assertEqual(unchoose(u1, linux), True)
        ed_choices1 = Choice.objects.filter(user=u1, option__question=qed)
        os_choices1 = Choice.objects.filter(user=u1, option__question=qos)
        ed_choices2 = Choice.objects.filter(user=u2, option__question=qed)
        os_choices2 = Choice.objects.filter(user=u2, option__question=qos)
        self.assertEqual(ed_choices1.count(), 0)
        self.assertEqual(os_choices1.count(), 0)
        self.assertEqual(ed_choices2.count(), 1)
        self.assertEqual(os_choices2.count(), 1)
        self.assertEqual(ed_choices2[0].option_id, vim.id)
        self.assertEqual(os_choices2[0].option_id, linux.id)

        self.assertEqual(vim.vote_count(), 1)
        self.assertEqual(linux.vote_count(), 1)

    def test_unchoose_other(self):
        u1 = User.objects.get(username='user1')
        u2 = User.objects.get(username='user2')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")
        atom = Option.objects.get(question=qed, text="Atom")
        windows = Option.objects.get(question=qos, text="Windows")

        self.assertEqual(choose(u1, vim), True)
        self.assertEqual(choose(u1, linux), True)
        self.assertEqual(choose(u2, vim), True)
        self.assertEqual(choose(u2, atom), True)
        self.assertEqual(choose(u2, linux), True)
        self.assertEqual(unchoose(u1, atom), False)
        self.assertEqual(unchoose(u1, windows), False)
        ed_choices1 = Choice.objects.filter(user=u1, option__question=qed)
        os_choices1 = Choice.objects.filter(user=u1, option__question=qos)
        ed_choices2 = Choice.objects.filter(user=u2, option__question=qed).order_by('id')
        os_choices2 = Choice.objects.filter(user=u2, option__question=qos).order_by('id')
        self.assertEqual(ed_choices1.count(), 1)
        self.assertEqual(os_choices1.count(), 1)
        self.assertEqual(ed_choices2.count(), 2)
        self.assertEqual(os_choices2.count(), 1)
        self.assertEqual(ed_choices1[0].option_id, vim.id)
        self.assertEqual(os_choices1[0].option_id, linux.id)
        self.assertEqual(ed_choices2[0].option_id, vim.id)
        self.assertEqual(ed_choices2[1].option_id, atom.id)
        self.assertEqual(os_choices2[0].option_id, linux.id)

        self.assertEqual(vim.vote_count(), 2)
        self.assertEqual(linux.vote_count(), 2)
        self.assertEqual(atom.vote_count(), 1)

    def test_locked(self):
        user = User.objects.get(username='user1')
        qed = Question.objects.get(title="Text Editor")
        qos = Question.objects.get(title="Operating System")
        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")
        atom = Option.objects.get(question=qed, text="Atom")

        self.assertEqual(choose(user, vim), True)
        self.assertEqual(choose(user, atom), True)
        self.assertEqual(choose(user, linux), True)

        qed.locked = True
        qed.save()
        qos.locked = True
        qos.save()

        vim = Option.objects.get(question=qed, text="Vim")
        linux = Option.objects.get(question=qos, text="Linux")
        atom = Option.objects.get(question=qed, text="Atom")
        sublime = Option.objects.get(question=qed, text="Sublime")
        windows = Option.objects.get(question=qos, text="Windows")

        self.assertEqual(unchoose(user, vim), None)
        self.assertEqual(unchoose(user, linux), None)
        self.assertEqual(unchoose(user, windows), None)
        self.assertEqual(choose(user, atom), None)
        self.assertEqual(choose(user, sublime), None)
        self.assertEqual(choose(user, windows), None)

        ed_choices = Choice.objects.filter(user=user, option__question=qed).order_by('id')
        os_choices = Choice.objects.filter(user=user, option__question=qos).order_by('id')
        self.assertEqual(ed_choices.count(), 2)
        self.assertEqual(os_choices.count(), 1)
        self.assertEqual(ed_choices[0].option_id, vim.id)
        self.assertEqual(ed_choices[1].option_id, atom.id)
        self.assertEqual(os_choices[0].option_id, linux.id)

        self.assertEqual(vim.vote_count(), 1)
        self.assertEqual(linux.vote_count(), 1)
        self.assertEqual(atom.vote_count(), 1)
        self.assertEqual(sublime.vote_count(), 0)
        self.assertEqual(windows.vote_count(), 0)

class TestAuth(TestCase):
    def setUp(self):
        User.objects.create_user('user1', password='pass1')
        u2 = User.objects.create_user('user2', password='pass2')
        u2.is_active = False
        u2.save()
        User.objects.create_user(s_anaar, password='pass1')
        uc = User.objects.create_user(s_chikoo, password='pass2')
        uc.is_active = False
        uc.save()
        populate.add_qlist(TEST_QLIST)

    def test_basic_auth_success(self):
        do_test_basic_auth(self, 'user1', 'pass1', 200, "[]")
        do_test_basic_auth(self, s_anaar, 'pass1', 200, "[]")
    def test_basic_auth_inactive(self):
        do_test_basic_auth(self, 'user2', 'pass2', 403, "inactive")
        do_test_basic_auth(self, s_chikoo, 'pass2', 403, "inactive")
    def test_basic_auth_wrong_login(self):
        do_test_basic_auth(self, 'user1', 'pass2', 401, "wrong_login")
        do_test_basic_auth(self, s_anaar, 'pass2', 401, "wrong_login")
    def test_basic_auth_bad_request(self):
        do_test_basic_auth(self, 'user1', 'pass1', 401, separator='**')
        do_test_basic_auth(self, s_anaar, 'pass1', 401, separator='**')

    def test_login_success(self):
        do_test_login(self, 'user1', 'pass1', 200, 200, FORM_CONTENT_TYPE, 'success')
        do_logout(self)
        do_test_login(self, 'user1', 'pass1', 200, 200, 'application/json', 'success')
        do_test_login(self, 'user1', 'pass1', 200, 200, output1='success')
        do_logout(self)
        do_test_login(self, s_anaar, 'pass1', 200, 200, FORM_CONTENT_TYPE, 'success')
        do_logout(self)
        do_test_login(self, s_anaar, 'pass1', 200, 200, 'application/json', 'success')
        do_test_login(self, 'user1', 'pass1', 200, 200, output1='success')
        do_logout(self)

    def test_login_inactive(self):
        do_test_login(self, 'user2', 'pass2', 200, 403, FORM_CONTENT_TYPE, 'inactive', 'inactive')
        do_logout(self)
        do_test_login(self, 'user2', 'pass2', 200, 403, 'application/json', 'inactive', 'inactive')
        do_test_login(self, 'user2', 'pass2', 200, 403, output1='inactive', output2='inactive')
        do_logout(self)
        do_test_login(self, s_chikoo, 'pass2', 200, 403, FORM_CONTENT_TYPE, 'inactive', 'inactive')
        do_logout(self)
        do_test_login(self, s_chikoo, 'pass2', 200, 403, 'application/json', 'inactive', 'inactive')
        do_test_login(self, s_chikoo, 'pass2', 200, 403, output1='inactive', output2='inactive')
        do_logout(self)

    def test_login_wrong(self):
        do_test_login(self, 'user1', 'pass2', 200, 401, FORM_CONTENT_TYPE, 'wrong_login', 'auth_missing')
        do_logout(self)
        do_test_login(self, 'user1', 'pass2', 200, 401, 'application/json', 'wrong_login', 'auth_missing')
        do_test_login(self, 'user1', 'pass2', 200, 401, output1='wrong_login', output2='auth_missing')
        do_logout(self)
        do_test_login(self, s_anaar, 'pass2', 200, 401, FORM_CONTENT_TYPE, 'wrong_login', 'auth_missing')
        do_logout(self)
        do_test_login(self, s_anaar, 'pass2', 200, 401, 'application/json', 'wrong_login', 'auth_missing')
        do_test_login(self, s_anaar, 'pass2', 200, 401, output1='wrong_login', output2='auth_missing')
        do_logout(self)

    def test_invalid_format1(self):
        do_test_login(self, 'user1', ['pass1'], 400, 401, # type: ignore # intentional type violation
                      "application/json", "invalid password format", 'auth_missing')
        do_test_login(self, ['user1'], 'pass1', 400, 401, # type: ignore # intentional type violation
                      "application/json", "invalid username format", 'auth_missing', login_username='user1')
        do_test_login(self, s_anaar, ['pass1'], 400, 401, # type: ignore # intentional type violation
                      "application/json", "invalid password format", 'auth_missing')
        do_test_login(self, [s_anaar], 'pass1', 400, 401, # type: ignore # intentional type violation
                      "application/json", "invalid username format", 'auth_missing', login_username=s_anaar)

    def test_invalid_format2(self):
        do_test_login(self, 'user1', 'pass1', 400, 401, "application/json", "invalid data format", "auth_missing", as_dict=False)
        do_test_login(self, s_anaar, 'pass1', 400, 401, "application/json", "invalid data format", "auth_missing", as_dict=False)

    def test_register_form1(self):
        do_test_register(self, 'user1', 'pass1', 200, "username_taken")
        do_test_register(self, 'user3', 'pass3', 200, "success")
        do_test_register(self, 'user3', 'pass1', 200, "username_taken")
        do_test_register(self, s_anaar, 'pass1', 200, "username_taken")

    def test_disallow_register_form1(self):
        with self.settings(ALLOW_REG=False):
            do_test_register(self, 'user1', 'pass1', 403, "reg_closed")
            do_test_register(self, s_anaar, 'pass1', 403, "reg_closed")
            do_test_register(self, 'user3', 'pass3', 403, "reg_closed")

    def test_disallow_register_json(self):
        with self.settings(ALLOW_REG=False):
            do_test_register(self, 'user1', 'pass1', 403, "reg_closed", "application/json")
            do_test_register(self, s_anaar, 'pass1', 403, "reg_closed", "application/json")
            do_test_register(self, 'user3', 'pass3', 403, "reg_closed", "application/json")

    def test_disallow_register_form2(self):
        with self.settings(ALLOW_REG=False):
            do_test_register(self, 'user1', 'pass1', 403, "reg_closed", FORM_CONTENT_TYPE)
            do_test_register(self, s_anaar, 'pass1', 403, "reg_closed", FORM_CONTENT_TYPE)
            do_test_register(self, 'user3', 'pass3', 403, "reg_closed", FORM_CONTENT_TYPE)

    def test_allow_register_form1(self):
        with self.settings(ALLOW_REG=True):
            do_test_register(self, 'user1', 'pass1', 200, "username_taken")
            do_test_register(self, 'user3', 'pass3', 200, "success")
            do_test_register(self, 'user3', 'pass3', 200, "username_taken")
            do_test_register(self, s_anaar, 'pass1', 200, "username_taken")

    def test_allow_register_json(self):
        with self.settings(ALLOW_REG=True):
            do_test_register(self, 'user1', 'pass1', 200, "username_taken", "application/json")
            do_test_register(self, 'user3', 'pass3', 200, "success", "application/json")
            do_test_register(self, 'user3', 'pass3', 200, "username_taken", "application/json")
            do_test_register(self, s_anaar, 'pass1', 200, "username_taken", "application/json")

    def test_allow_register_form2(self):
        with self.settings(ALLOW_REG=True):
            do_test_register(self, 'user1', 'pass1', 200, "username_taken", FORM_CONTENT_TYPE)
            do_test_register(self, 'user3', 'pass3', 200, "success", FORM_CONTENT_TYPE)
            do_test_register(self, 'user3', 'pass3', 200, "username_taken", FORM_CONTENT_TYPE)
            do_test_register(self, s_anaar, 'pass1', 200, "username_taken", FORM_CONTENT_TYPE)

class TestApiViews(TestCase):
    def setUp(self):
        User.objects.create_user('user1', password='pass1')
        User.objects.create_user('user2', password='pass2')
        User.objects.create_user('user3', password='pass3')
        populate.add_qlist(TEST_QLIST)

    def test_all_ques(self):
        response = self.client.get('/api/')
        response_dict = json.loads(get_response_str(response))
        file_dict = json.load(open(TEST_DATA_FILE))
        self.assertEqual(response_dict, file_dict)

    def test_my_choices_unauthed(self):
        response = self.client.get('/api/my-choices/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(get_response_str(response), 'auth_missing')

    def test_my_choices_empty(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)
        response = self.client.get('/api/my-choices/')
        self.assertEqual(response.status_code, 200)
        choices = json.loads(get_response_str(response))
        self.assertEqual(choices, [])

    def test_my_choices_one(self):
        user = User.objects.get(username='user1')
        vim = Option.objects.get(text="Vim")
        choose(user, vim)

        self.client.force_login(user)
        response = self.client.get('/api/my-choices/')
        self.assertEqual(response.status_code, 200)
        choices = json.loads(get_response_str(response))
        self.assertEqual(choices, [vim.id])

    def test_my_choices_many(self):
        user = User.objects.get(username='user1')
        vim = Option.objects.get(text="Vim")
        linux = Option.objects.get(text="Linux")
        choose(user, vim)
        choose(user, linux)

        self.client.force_login(user)
        response = self.client.get('/api/my-choices/')
        self.assertEqual(response.status_code, 200)
        choices = json.loads(get_response_str(response))
        self.assertEqual(choices, sorted([vim.id, linux.id]))

    def test_questions(self):
        response = self.client.get('/api/questions/')
        response_str = get_response_str(response)
        data = json.loads(response_str)
        for (id, qdict) in six.iteritems(data):
            ques = Question.objects.get(id=id)
            for (key, value) in six.iteritems(qdict):
                self.assertEqual(qdict[key], getattr(ques, key))

    def test_options(self):
        response = self.client.get('/api/options/')
        response_str = get_response_str(response)
        data = json.loads(response_str)
        for (id, odict) in six.iteritems(data):
            option = Option.objects.get(id=id)
            self.assertEqual(odict["text"], option.text)
            self.assertEqual(odict["question"], option.question_id)
            if option.question.show_count:
                self.assertEqual(odict["count"], option.vote_count())
                self.assertEqual(odict["count"], 0)
            else:
                self.assertIsNone(odict["count"])

    def test_vote_form_empty(self):
        do_test_vote(self, "user1", None, None, None, 200, [])
        do_test_vote(self, "user2", None, None, None, 200, [], "application/json")
        do_test_vote(self, "user3", None, None, None, 200, [], FORM_CONTENT_TYPE)
        do_test_vote(self, "user1", None, None, None, 200, [], "application/json;")
        do_test_vote(self, "user2", None, None, None, 200, [], FORM_CONTENT_TYPE + ";")

    def test_vote_choose_only(self):
        do_test_vote(self, "user1", ["Vim", "Windows"], ["Vim", "Linux"], None, 200, ["Vim", "Linux"])
        do_test_vote(self, "user2", ["Vim", "Windows"], ["Vim", "Linux"], None, 200, ["Vim", "Linux"], "application/json")
        do_test_vote(self, "user3", ["Vim", "Windows"], ["Vim", "Linux"], None, 200, ["Vim", "Linux"], FORM_CONTENT_TYPE)

    def test_vote_unchoose_only(self):
        do_test_vote(self, "user1", ["Vim", "Atom"], None, ["Vim", "Linux"], 200, ["Atom"])
        do_test_vote(self, "user2", ["Vim", "Atom"], None, ["Vim", "Linux"], 200, ["Atom"], "application/json")
        do_test_vote(self, "user3", ["Vim", "Atom"], None, ["Vim", "Linux"], 200, ["Atom"], FORM_CONTENT_TYPE)

    def test_vote_both(self):
        do_test_vote(self, "user1", ["Vim", "Sublime"], ["Atom"], ["Sublime"], 200, ["Vim", "Atom"])
        do_test_vote(self, "user2", ["Vim", "Sublime"], ["Atom"], ["Sublime"], 200, ["Vim", "Atom"], "application/json")
        do_test_vote(self, "user3", ["Vim", "Sublime"], ["Atom"], ["Sublime"], 200, ["Vim", "Atom"], FORM_CONTENT_TYPE)

    def test_vote_inboth(self):
        do_test_vote(self, "user1", ["Vim", "Sublime"], ["Vim", "Atom"], ["Vim"], 400, ["Vim", "Sublime"])
        do_test_vote(self, "user2", ["Vim", "Sublime"], ["Vim", "Atom"], ["Vim"], 400, ["Vim", "Sublime"], "application/json")
        do_test_vote(self, "user3", ["Vim", "Sublime"], ["Vim", "Atom"], ["Vim"], 400, ["Vim", "Sublime"], FORM_CONTENT_TYPE)

    def test_vote_num_choose_only(self):
        do_test_vote(self, "user1", ["Vim", "Windows"], ["Vim", "Linux"], None, 200, ["Vim", "Linux"], "application/json", True)

    def test_vote_num_unchoose_only(self):
        do_test_vote(self, "user1", ["Vim", "Atom"], None, ["Vim", "Linux"], 200, ["Atom"], "application/json", True)

    def test_vote_num_both(self):
        do_test_vote(self, "user2", ["Vim", "Sublime"], ["Atom"], ["Sublime"], 200, ["Vim", "Atom"], "application/json", True)

    def test_vote_num_inboth(self):
        do_test_vote(self, "user2", ["Vim", "Sublime"], ["Vim", "Atom"], ["Vim"], 400, ["Vim", "Sublime"], "application/json", True)

    def test_vote_locked_form1(self):
        do_test_vote(self, "user1", ["Vim", "Sublime", "Windows"], ["Atom", "Linux"], ["Sublime"],
                     200, ["Vim", "Sublime", "Linux"], locked_titles=["Text Editor"])
    def test_vote_locked_json(self):
        do_test_vote(self, "user2", ["Vim", "Sublime", "Windows"], ["Atom", "Linux"], ["Sublime"],
                     200, ["Vim", "Sublime", "Linux"], "application/json", locked_titles=["Text Editor"])
    def test_vote_locked_form2(self):
        do_test_vote(self, "user3", ["Vim", "Sublime", "Windows"], ["Atom", "Linux"], ["Sublime"],
                     200, ["Vim", "Sublime", "Linux"], FORM_CONTENT_TYPE, locked_titles=["Text Editor"])
