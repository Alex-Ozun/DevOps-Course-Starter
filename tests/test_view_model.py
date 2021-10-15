import pytest

from todo_app.data.view_model import ViewModel
from todo_app.data.trello_api import Card

def test_viewmodel_todo_cards():
    """Test that the ViewModel returns the items from the "To Do" list."""
    card = Card(id='123', list_id='123', title='Hello', checked=False)
    viewModel = ViewModel(all_cards=[card])
    todo_cards = viewModel.todo_cards()
    assert len(todo_cards) == 1
    assert todo_cards[0].id == '123'

def test_viewmodel_done_cards():
    """Test that the ViewModel returns the items from the "Done" list."""
    card = Card(id='123', list_id='123', title='Hello', checked=True)
    viewModel = ViewModel(all_cards=[card])
    done_cards = viewModel.done_cards()
    assert len(done_cards) == 1
    assert done_cards[0].id == '123'
