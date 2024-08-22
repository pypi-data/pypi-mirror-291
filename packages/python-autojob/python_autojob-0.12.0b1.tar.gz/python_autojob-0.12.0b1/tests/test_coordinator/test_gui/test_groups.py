# import pytest

# from autojob.coordinator.gui.groups import StructureGroup
# from tests.accountant.datasource import DataSource


# class TestStructureGroup:
#     @staticmethod
#     def test_structures():
#         group = StructureGroup()
#         group.structures = DataSource.structures

#         for structure in group.structures:
#             assert structure in DataSource.structures

#         for structure in DataSource.structures:
#             assert structure in group.structures

#     @staticmethod
#     @pytest.mark.parametrize('new_structures', [0, True])
#     def test_validate_structures_one(new_structures):
#         group = StructureGroup()
#         with pytest.raises(TypeError) as exc_info:
#             group.structures = new_structures

#         assert 'iterable' in exc_info.value.args[0]

#     @staticmethod
#     @pytest.mark.parametrize('new_structures', [[0], [True]])
#     def test_validate_structures_two(new_structures):
#         group = StructureGroup()
#         with pytest.raises(ValueError) as exc_info:
#             group.structures = new_structures

#         assert 'Path or str' in exc_info.value.args[0]

#     @staticmethod
#     @pytest.mark.parametrize('new_structures', [['xxx']])
#     def test_validate_structures_three(new_structures):
#         group = StructureGroup()
#         with pytest.raises(FileNotFoundError) as exc_info:
#             group.structures = new_structures

#         assert 'does not exist' in exc_info.value.args[0]

#     @staticmethod
#     @pytest.mark.parametrize('new_structures', [['.']])
#     def test_validate_structures_four(new_structures):
#         group = StructureGroup()
#         with pytest.raises(ValueError) as exc_info:
#             group.structures = new_structures

#         assert 'must be a file' in exc_info.value.args[0]
