[Setup]
AppName=NOVA
AppVersion=1.0.0
AppPublisher=NOVA
DefaultDirName={autopf}\NOVA
DefaultGroupName=NOVA
OutputDir=C:\Users\sc\Desktop\NOVA\Installer
OutputBaseFilename=NOVA_Setup
SetupIconFile=C:\Users\sc\Desktop\NOVA\nova_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Files]
Source: "C:\Users\sc\Desktop\NOVA\dist\NOVA\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\NOVA"; Filename: "{app}\NOVA.exe"
Name: "{autodesktop}\NOVA"; Filename: "{app}\NOVA.exe"

[Run]
Filename: "{app}\NOVA.exe"; Description: "Launch NOVA"; Flags: nowait postinstall skipifsilent