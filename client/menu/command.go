package menu

// Command struct allows you control your command
type action func(s *State, menuDict map[string]Menu) error

type Command struct {
	Name    string
	Handler action
}
