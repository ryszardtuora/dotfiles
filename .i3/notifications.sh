env DBUS_SESSION_BUS_ADDRESSS=unix:path=/run/user/1000/bus
env XDG_RUNTIME_DIR=/run/user/$(id -u)
appointments=$( /usr/bin/calcurse -d 7 )

if [[ ! -z $appointments ]]
then
/usr/bin/notify-send "Appointments:" "$appointments"
fi
