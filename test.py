from context_menu import menus

fc = menus.FastCommand('Send To Home', type='FILES', command='Z: && cd Z:\\Documents\\moritz_tools && python send_to_home_sc.py')
fc.compile()
