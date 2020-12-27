package menu

// State struct allows you control your state
type State struct {
	menu Menu
	MenuDict map[string]Menu
}

func (s State) GetMenu() Menu {
	return s.menu
}

func (s *State) SetMenu(newMenu Menu) {
	s.menu = newMenu
}
