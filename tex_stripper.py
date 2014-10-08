import shutil, sys, os, string, re
from numpy import *

# file to be processed
f = sys.argv[1]

if os.path.exists(f):
    lines = file(f).readlines()
else:
    print 'File Not Found'
    sys.exit()

if not f[-4:] == '.tex':
    print 'File must be .tex'
    sys.exit()

# things that should be removed with no partner
keys = ['\section','\sub','\label','\chapter']

# things that should be removed that have partners
start_keys = [r'\begin{figure','\[',r'\begin{equation','$$',r'\begin{table',r'\begin{itemize',r'\begin{eqn']
end_keys = ['\end{figure','\]','\end{equation','$$','\end{table',r'\end{itemize',r'\end{eqn']

# lines with line_flag = 0 will be written
# lines with line_flag = 1 will not
line_flag = zeros(len(lines))
iline = -1
for line in lines:

    iline += 1
    
    # check if already flagged
    if line_flag[iline] == 1:
        continue

    # check for strings in keys
    for ikey in range(len(keys)):
        if any(keys[ikey] in line):
            line_flag[iline] = 1
            continue

    # check if line starts with '%'
    if line[0] == '%':
        line_flag[iline] = 1
        continue
    
    # check for strings in start_keys
    for ikey in range(len(start_keys)):
        if start_keys[ikey] in line:
            # search for end_keys
            delta = 1
            for line2 in lines[iline+1:]:
                if end_keys[ikey] in line2:
                    # get rid of lines in between start and end keys
                    line_flag[iline:iline+delta+1] = 1
                    break
                else:
                    delta += 1

# write back out
of = open(f[:-4]+'_stripped.tex','w')
for iline in range(len(lines)):
    if line_flag[iline] == 0:
        # replace inline math
        line = lines[iline]
        line = re.sub(r'\$(.+?)\$', r'x = 1', line)
        # replace citation
        line = re.sub(r'\\cite{(.+?)\}', r'[1]', line)
        # replace references
        line = re.sub(r'\\ref{(.+?)\}', r'1', line)
        of.write(line)

of.close()
