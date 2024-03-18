import os
import unittest
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field

from prompts import SYSTEM_MESSAGE, HUMAN_MESSAGE_EXT_DATA, EMAIL_CONTENT_SAMPLE, HUMAN_MESSAGE_GEN_MAIL, all_info_ext_req
from data_class import AllInfo, AGT, Customer

load_dotenv(verbose=True)
dotenv_path = os.path.join('../.env')
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
print("using model:", OPENAI_MODEL)


class MailAssistant:
    def __init__(self) -> None:
        self.mail_data_parser = PydanticOutputParser(pydantic_object=AllInfo)
        self.system_prompt_template = SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE)
        self.model = ChatOpenAI(model_name=OPENAI_MODEL)
        parse_mail_human_prompt_template = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=HUMAN_MESSAGE_EXT_DATA,
                input_variables=["email_content", "request"],
                partial_variables={"format_instructions": self.mail_data_parser.get_format_instructions()}
            )
        )
        parse_mail_chat_prompt = ChatPromptTemplate.from_messages([self.system_prompt_template, parse_mail_human_prompt_template])
        self.parse_mail_chain = LLMChain(llm=self.model, prompt=parse_mail_chat_prompt)
        gen_mail_human_message_templ = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=HUMAN_MESSAGE_GEN_MAIL,
                input_variables=["email_content", "lacked_info"],
            )
        )
        gen_mail_chat_prompt = ChatPromptTemplate.from_messages([self.system_prompt_template, gen_mail_human_message_templ])
        self.gen_mail_chain = LLMChain(llm=self.model, prompt=gen_mail_chat_prompt)

    def _list_none_attributes(self, instance: AllInfo):
        none_attributes = {}
        for field in instance.model_fields:
            value = getattr(instance, field)
            if value is None:
                none_attributes[field] = None
            elif isinstance(value, (AGT, Customer)):
                none_attrs = self._list_none_attributes(value)
                none_attributes[field] = none_attrs
        return none_attributes
    

    def parse_mail(self, email_content):
        all_parse_mail_chain = SequentialChain(chains=[self.parse_mail_chain], input_variables=["email_content", "request"], verbose=True)
        parse_mail_ans = all_parse_mail_chain({'email_content':email_content, 'request':all_info_ext_req})
        out = parse_mail_ans['text'].replace("None", "null")
        fix_parser = OutputFixingParser.from_llm(parser=self.mail_data_parser, llm=ChatOpenAI(model_name=OPENAI_MODEL))
        parsed_data = fix_parser.parse(out)
        return parsed_data
    
    def gen_mail(self, email_content, parsed_data):
        none_attributes = self._list_none_attributes(parsed_data)

        def create_none_attr_list_str(none_attributes):
            output = ''
            if len(none_attributes['intermediate_company_info']):
                output += 'from intermediate company information:\n'
                for k in none_attributes['intermediate_company_info'].keys():
                    output += f'- {k}\n'
            if len(none_attributes['customer_info']):
                output += 'from customer information:\n'
                for k in none_attributes['customer_info'].keys():
                    output += f'- {k}\n'
            return output
        
        none_str = create_none_attr_list_str(none_attributes)

        all_gen_mail_chain = SequentialChain(chains=[self.gen_mail_chain], input_variables=["email_content", "lacked_info"], verbose=True)
        gen_mail_ans = all_gen_mail_chain({'email_content':email_content, 'lacked_info': none_str})
        generated_mail = gen_mail_ans['text']
        return none_str, generated_mail


class TestMailAssistant(unittest.TestCase):
    def setUp(self) -> None:
        self.mail_assistant = MailAssistant()
        self.email_content = EMAIL_CONTENT_SAMPLE

    def test_parse_mail(self):
        parsed_data:AllInfo = self.mail_assistant.parse_mail(self.email_content)
        print(parsed_data.model_dump_json())
    
    def test_gen_mail(self):
        parsed_data = self.mail_assistant.parse_mail(self.email_content)
        none_str, gened_mail = self.mail_assistant.gen_mail(self.email_content, parsed_data)
        print(none_str)
        print(gened_mail)
        