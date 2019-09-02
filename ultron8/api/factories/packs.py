# from factory import Faker, LazyFunction, Sequence, LazyAttribute
# from ultron8.api.factories.base import BaseFactory, fake, pack_name_list
# from ultron8.api.models.packs import PacksData

# def random_pack_name():
#     return f"{fake.pack_name()}"

# def random_description():
#     return f"{fake.sentance()}"

# class PacksFactory(BaseFactory):
#     class Meta:
#         model = PacksData

#     # name = LazyFunction(random_pack_name)
#     name = fake.word(ext_word_list=pack_name_list)
#     # description = fake.sentance()
#     description = LazyFunction(fake.sentance)
#     keywords = LazyAttribute(lambda obj: '%s' % obj.name)
#     version = "0.1.0"
#     python_versions = "3"
#     author = "Jarvis"
#     email = fake.email()
#     contributors = fake.first_name()
#     files = LazyAttribute(lambda obj: "./tests/fixtures/simple/packs/%s" % obj.name)
#     path = LazyAttribute(lambda obj: "./tests/fixtures/simple/packs/%s" % obj.name)

# # smoke test
# if __name__ == "__main__":
#     from ultron8.debugger import debug_dump_exclude
#     # import pdb;pdb.set_trace()
#     p = PacksFactory()
#     print(p)
