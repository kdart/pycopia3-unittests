#!/usr/bin/python
# vim:ts=4:sw=4:softtabstop=0:smarttab

"""
Basic database tests
--------------------
"""

import peewee

from pycopia.QA import core
from pycopia.QA import constants

# Module under test
from pycopia.QA.db import models


class GetMetadata(core.TestCase):
    """Get a tables metadata."""

    def execute(self):
        md = models.get_metadata(models.Equipment)[0]
        if not isinstance(md, peewee.ColumnMetadata):
            self.diagnostic("Not ColumnMetadata: {!r}".format(md))
            return self.failed("Not ColumnMetadata")
        colmd = models.get_column_metadata(models.Equipment, "name")
        self.assertEqual(colmd.name, "name")
        self.passed("Got proper metadata")


class PrimaryKeys(core.TestCase):
    """Check primary key introspection."""

    def execute(self):
        self.assertEqual(models.get_primary_key_name(models.Equipment), "id")
        self.assertEqual(models.get_primary_key_name(models.ClientSession), "session_key")
        self.passed("Got proper primary key names")


class CheckConfig(core.TestCase):
    """QC mock configuration table."""

    def execute(self):
        self.assertEqual(self.config.resultsdirbase,
                '/var/www/localhost/htdocs/testresults')
        self.passed("Config values set.")


class CreateAttributeTypes(core.TestCase):
    """Test create attribute types."""

    def execute(self):
        with models.database.atomic():
            for name, vtype, desc in (
                ("objecttype",constants.ValueType.Object, "Object type."),
                ("accessmethod", constants.ValueType.String, "A string value type."),
                ("initial_accessmethod", constants.ValueType.String, "A string value type."),
                ("integertype", constants.ValueType.Integer, "Integer type."),
                ("floattype", constants.ValueType.Float, "Float type."),
                ("booleantype", constants.ValueType.Boolean, "Boolean type."),
                ):
                models.AttributeType.create(name=name, value_type=vtype,
                    description=desc)
        self.assertEqual(len(list(models.AttributeType.get_attribute_list())), 6)
        self.passed("Created AttributeType")


class CreateUser(core.TestCase):
    """Create a User."""

    def execute(self):
        with models.database.atomic():
            models.User.create(first_name="A", last_name="User",
                username="auser", authservice="system")
        user = models.User.select().first()
        user.password = "password123"
        self.assertEqual(user.password, "password123")
        auser = models.User.get_by_username("auser")
        self.assertEqual(auser.username, "auser")
        self.info(auser)
        self.passed("Created user with password")


class CreateFunction(core.TestCase):
    """Create a Function."""

    def execute(self):
        with models.database.atomic():
            models.Function.create(name="tester", description="A tester thing.")
        func = models.Function.select().first()
        self.assertEqual(func.name, "tester")
        func = models.Function.get_by_name("tester")
        self.assertEqual(func.name, "tester")
        self.assertRaises(models.ModelError,
                          models.Function.get_by_name, args=("xxx",),
                          msg="Failed to raise ModelError.")
        self.passed("Created a function")


class CreateMisc(core.TestCase):
    """Create support data for other tests."""
    PREREQUISITES = ["CreateFunction"]

    def execute(self):
        with models.database.atomic():
            models.InterfaceType.create(name="ethernetCsmacd",
                                        enumeration=6)
            models.AuthGroup.create(name="testers",
                                    description="Group that performs tests.")
            models.Networks.create(name="local", ipnetwork="192.168.1.0/24",
                                   layer=3)
        self.passed("Misc created.")


class CreateCorp(core.TestCase):
    """Create a Corporation."""

    def execute(self):
        with models.database.atomic():
            models.Corporations.create(name="Acme Coyote Supplies")
        corp = models.Corporations.select().first()
        self.passed("Added Corporation {}.".format(corp.name))


class CreateEquipmentModel(core.TestCase):
    """."""
    PREREQUISITES = ["CreateCorp"]

    def execute(self):
        corp = models.Corporations.select().first()
        with models.database.atomic():
            models.EquipmentModel.create(name="MyModel", manufacturer=corp)
            models.EquipmentModel.create(name="Tester", manufacturer=corp)
        self.passed("Added equipment models.")


class CreateEquipment(core.TestCase):
    """."""
    PREREQUISITES = ["CreateEquipmentModel"]

    def execute(self):
        EQM = models.EquipmentModel
        mymodel = EQM.select().where(EQM.name == "MyModel").get()
        testmodel = EQM.select().where(EQM.name == "Tester").get()
        with models.database.atomic():
            models.Equipment.create(name="equipment.local", model=mymodel)
            models.Equipment.create(name="altequipment.local", model=mymodel)
            models.Equipment.create(name="tester.local", model=testmodel)
        eq = models.Equipment.select().first()
        self.assertEqual(eq.name, "equipment.local")
        self.passed("Added equipment.")


class CreateTestEquipment(core.TestCase):
    """."""
    PREREQUISITES = ["CreateEquipment"]

    def execute(self):
        ENV = models.Environments
        env = ENV.select().where(ENV.name=="default").get()
        eq = models.Equipment.select().first()
        with models.database.atomic():
            models.Testequipment.create(equipment=eq, environment=env, DUT=True)
        te = models.Testequipment.select().first()
        self.assertTrue(te.DUT)
        self.passed("Added Testequipment (DUT)")


class EquipmentAttribute(core.TestCase):
    """Set and get equipment attribute."""
    PREREQUISITES = ["CreateEquipment"]

    def execute(self):
        eq = models.Equipment.select().first()
        eq.set_attribute("accessmethod", "testme")
        attr = eq.get_attribute("accessmethod")
        self.assertEqual(attr, "testme")
        self.assertEqual(len(list(eq.attributes)), 1)
        self.passed("set and retrieved equipment attribute")


class EnvironmentFunctions(core.TestCase):
    """Check environment functions."""
    PREREQUISITES = ["CreateTestEquipment"]

    def execute(self):
        ENV = models.Environments
        EQ = models.Equipment
        env = ENV.select().where(ENV.name=="default").get()
        self.info(env.name)
        eq = EQ.select().where(EQ.name == "tester.local").get()
        env.add_testequipment(eq, "tester")
        roles = env.get_supported_roles()
        self.assertTrue("tester" in roles)
        dut = env.get_DUT()
        self.assertEqual(dut.name, "equipment.local", "Didn't get DUT")
        eq = env.get_equipment_with_role("tester")
        self.assertEqual(dut.name, "tester.local", "Didn't get tester")
        self.assertRaises(models.ModelError,
                          env.get_equipment_with_role, args=("xxx",),
                          msg="Failed to raise ModelError.")
        self.passed("Functions passed")


class EquipmentInterfaces(core.TestCase):
    """Check environment functions."""
    PREREQUISITES = ["CreateEquipment"]

    def execute(self):
        EQ = models.Equipment
        eq = EQ.select().where(EQ.name == "tester.local").get()
        eq.add_interface("eth1", interface_type="ethernetCsmacd",
                         ipaddr="192.168.1.2/24")
        self.assertEqual(len(list(eq.interfaces)), 1)
        eq.del_interface("eth1")
        self.assertEqual(len(list(eq.interfaces)), 0)
        eq.add_interface("eth1", interface_type="ethernetCsmacd",
                         ipaddr="192.168.1.2/24", network="local")
        self.assertEqual(len(list(eq.interfaces)), 1)
        self.passed("Added interface")


class XXX(core.TestCase):
    """."""
    #PREREQUISITES = [""]

    def execute(self):
        #self.assertEqual()
        self.passed("XXX")


class DatabaseUseCase(core.UseCase):
    """Database creation tests.
    """

    @staticmethod
    def get_suite(config, environment, ui):
        suite = core.TestSuite(config, environment, ui, name="DatabaseSuite")
        suite.add_tests([
            GetMetadata,
            CheckConfig,
            PrimaryKeys,
            CreateAttributeTypes,
            CreateFunction,
            CreateMisc,
            CreateUser,
            CreateCorp,
            CreateEquipmentModel,
            CreateEquipment,
            EquipmentAttribute,
            CreateTestEquipment,
            EnvironmentFunctions,
            EquipmentInterfaces,
            ])
        return suite



    # print(get_choices(Equipment, "interfaces", order_by=None))
    # print(Equipment.interfaces)
    # print(eq.attributes)
    # print("Interfaces:")
    # print(eq.interfaces)

#    for res in TestResults.get_latest_results():
#        print (res)

#    lr = TestResults.get_latest_run(user)
#    print(lr)
#    tc = TestCase.get_by_implementation(
#           "testcases.unittests.WWW.client.HTTPPageFetch")
#    print(tc)
#    print(get_primary_key_value(tc))
#    ltr = tc.get_latest_result()
#    print(ltr)
#
#    for tr in tc.get_data():
#        print(tr)

