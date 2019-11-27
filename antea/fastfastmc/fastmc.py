#
# The fast MC generates pairs of interaction points based on
#  pre-determined matrices of true r, phi, and z coordinates vs. their
#  reconstructed error. It uses the true information coming from GEANT4 simulations
#

import numpy  as np
import pandas as pd

from antea.fastfastmc.errmat import errmat
import antea.reco.reco_functions as rf

def simulate_reco_event(evt_id: int, hits: pd.DataFrame, particles: pd.DataFrame,
                        errmat_r: errmat, errmat_phi: errmat, errmat_z: errmat) -> pd.DataFrame:
    """
    Simulate the reconstructed coordinates for 1 coincidence from true GEANT4 dataframes.
    """

    evt_parts = particles[particles.event_id == evt_id]
    evt_hits  = hits     [hits.event_id      == evt_id]

    pos1, pos2, t1, t2 = rf.find_first_interactions_in_active(evt_parts, evt_hits)

    if len(pos1) == 0 or len(pos2) == 0:
        return None

    # Transform in cylindrical coordinates
    cyl_pos = rf.from_cartesian_to_cyl(np.array([pos1, pos2]))

    r1   = cyl_pos[0, 0]
    phi1 = cyl_pos[0, 1]
    z1   = cyl_pos[0, 2]
    r2   = cyl_pos[1, 0]
    phi2 = cyl_pos[1, 1]
    z2   = cyl_pos[1, 2]

    # Get all errors.
    er1 = errmat_r.get_random_error(r1)
    er2 = errmat_r.get_random_error(r2)
    ephi1 = errmat_phi.get_random_error(phi1)
    ephi2 = errmat_phi.get_random_error(phi2)
    ez1 = errmat_z.get_random_error(z1)
    ez2 = errmat_z.get_random_error(z2)
    
    # Compute reconstructed quantities.
    r1_reco = r1 - er1
    r2_reco = r2 - er2
    phi1_reco = phi1 - ephi1
    phi2_reco = phi2 - ephi2
    z1_reco = z1 - ez1
    z2_reco = z2 - ez2

    events    = [evt_id]

    true_r1   = [r1]
    true_phi1 = [phi1]
    true_z1   = [z1]
    true_r2   = [r2]
    true_phi2 = [phi2]
    true_z2   = [z2]

    reco_r1   = [r1_reco]
    reco_phi1 = [phi1_reco]
    reco_z1   = [z1_reco]
    reco_r2   = [r2_reco]
    reco_phi2 = [phi2_reco]
    reco_z2   = [z2_reco]

    events = pd.DataFrame({'event_id':  events,
                           'true_r1':   true_r1,
                           'true_phi1': true_phi1,
                           'true_z1':   true_z1,
                         #  'true_t1':   a_true_t1,
                           'true_r2':   true_r2,
                           'true_phi2': true_phi2,
                           'true_z2':   true_z2,
                       #    'true_t2':   a_true_t2,
                           'reco_r1':   reco_r1,
                           'reco_phi1': reco_phi1,
                           'reco_z1':   reco_z1,
                           'reco_r2':   reco_r2,
                           'reco_phi2': reco_phi2,
                           'reco_z2':   reco_z2})
    return events
