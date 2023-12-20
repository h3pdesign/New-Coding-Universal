on setDarkMode(shouldBeDark)
	
	set paneID to "com.apple.preference.general"
	
	tell application "System Events"
		if dark mode of appearance preferences is shouldBeDark then return
	end tell
	
	set paneWasOpen to false
	
	(*
		If SysPrefs is already running and showing the "General" pane,
		then toggling dark mode causes the UI of the pane to become
		out-of-sync with actual system appearance. To account for this,
		we'll quit SysPrefs if it's open to General prefs, and then
		re-open it after we've made the change
	*)
	if application "System Preferences" is running then
		tell application "System Preferences"
			if show all is false and id of current pane is paneID then
				set paneWasOpen to true
				quit
			end if
		end tell
	end if
	
	tell application "System Events"
		set dark mode of appearance preferences to shouldBeDark
	end tell
	
	if paneWasOpen then
		tell application "System Preferences"
			launch
			delay 3
			activate
			reveal (the first pane whose id is paneID)
		end tell
	end if
	
end setDarkMode

set result to display dialog "Set System Appearance" buttons ["Light Mode", "Dark Mode"]
if button returned of result is "Light Mode" then
	setDarkMode(false)
else
	setDarkMode(true)
end if