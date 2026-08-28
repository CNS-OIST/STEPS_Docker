import steps.interface
from steps.model import *
from steps.geom import *
from steps.rng import *
from steps.sim import *
from steps.saving import *
import numpy, steps

# The optional stack the image exists to provide: MPI, PETSc and parallel HDF5.
import h5py, mpi4py, petsc4py
petsc4py.init()
from petsc4py import PETSc
assert h5py.get_config().mpi, 'h5py was built without MPI support'
print('h5py', h5py.__version__, '| mpi4py', mpi4py.__version__, '| petsc4py', petsc4py.__version__)

mdl = Model()
with mdl:
    S1, S2, S3 = Species.Create()
    vsys = VolumeSystem.Create()
    r = ReactionManager()
    with vsys:
        S1 + S2 <r['r1']> S3
        r['r1'].K = 1e6, 10

geom = Geometry()
with geom:
    comp = Compartment.Create(vsys, 1e-18)

rng = RNG('mt19937', 512, 1234)
for solver in ['Wmdirect', 'Wmrssa', 'Wmrk4']:
    sim = Simulation(solver, mdl, geom, rng)
    rs = ResultSelector(sim)
    sel = rs.comp.LIST(S1, S2, S3).Count
    sim.toSave(sel, dt=0.01)
    sim.newRun()
    if solver == "Wmrk4": sim.setDT(1e-5)
    sim.comp.S1.Count = 100
    sim.comp.S2.Count = 100
    sim.run(0.1)
    d = sel.data[0]
    print(f'{solver}: shape={d.shape} final={d[-1]} dtype={d.dtype}')
print('steps', steps.__version__, '| numpy', numpy.__version__, '| RECORDING OK')
