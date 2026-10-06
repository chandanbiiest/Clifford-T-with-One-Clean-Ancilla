OPENQASM 2.0;
include "qelib1.inc";
qreg q[5];
creg out[1];
// q[0],q[1],q[2] controls; q[3] clean ancilla; q[4] target.
// Structural reference using CCX instructions. Provider compilation determines native gates.
ccx q[0],q[1],q[3];
ccx q[3],q[2],q[4];
ccx q[0],q[1],q[3];
measure q[4] -> out[0];
