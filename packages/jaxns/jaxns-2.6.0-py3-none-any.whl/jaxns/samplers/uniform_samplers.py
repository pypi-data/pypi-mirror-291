from typing import NamedTuple, Tuple

import jax
from jax import random, numpy as jnp, lax

from jaxns.framework.bases import BaseAbstractModel
from jaxns.internals.types import IntArray, StaticStandardNestedSamplerState, UType, MeasureType, \
    StaticStandardSampleCollection
from jaxns.internals.types import PRNGKey, FloatArray
from jaxns.internals.types import Sample, int_type
from jaxns.samplers.abc import SamplerState
from jaxns.samplers.bases import BaseAbstractRejectionSampler

__all__ = [
    'UniformSampler'
]


class UniformSampler(BaseAbstractRejectionSampler):
    """
    A sampler that produces uniform samples from the model within the log_L_constraint.
    """

    def __init__(self, model: BaseAbstractModel, max_likelihood_evals: int = 100):
        """
        Initialises the sampler.

        Args:
            model: the model to sample from
            max_likelihood_evals: the maximum number of likelihood evaluations to perform, before stopping. This is
                important for not getting stuck on plateaus, or forbidden zones.
        """
        super().__init__(model=model)
        if max_likelihood_evals < 1:
            raise ValueError("max_likelihood_evals must be >= 1")
        self.max_likelihood_evals = int(max_likelihood_evals)

    def num_phantom(self) -> int:
        return 0

    def pre_process(self, state: StaticStandardNestedSamplerState) -> SamplerState:
        return ()

    def post_process(self, sample_collection: StaticStandardSampleCollection,
                     sampler_state: SamplerState) -> SamplerState:
        return sampler_state

    def get_sample(self, key: PRNGKey, log_L_constraint: FloatArray, sampler_state: SamplerState) -> Tuple[
        Sample, Sample]:
        class CarryState(NamedTuple):
            key: PRNGKey
            U: UType
            log_L: MeasureType
            num_likelihood_evals: IntArray

        def cond(carry_state: CarryState):
            done_1 = carry_state.log_L > log_L_constraint
            done_2 = jnp.bitwise_or(
                carry_state.log_L == log_L_constraint,
                carry_state.num_likelihood_evals >= self.max_likelihood_evals
            )
            done = jnp.bitwise_or(done_1, done_2)
            return jnp.bitwise_not(done)

        def body(carry_state: CarryState) -> CarryState:
            key, sample_key = random.split(carry_state.key, 2)
            U = self.model.sample_U(key=sample_key)
            log_L = self.model.forward(U=U)
            num_likelihood_evals = carry_state.num_likelihood_evals + jnp.ones_like(carry_state.num_likelihood_evals)
            return CarryState(key=key, U=U, log_L=log_L, num_likelihood_evals=num_likelihood_evals)

        key, sample_key = random.split(key, 2)
        init_U = self.model.sample_U(key=sample_key)
        init_log_L = self.model.forward(init_U)
        init_carry_state = CarryState(
            key=key,
            U=init_U,
            log_L=init_log_L,
            num_likelihood_evals=jnp.asarray(1, int_type)
        )

        carry_state = lax.while_loop(cond_fun=cond, body_fun=body, init_val=init_carry_state)

        sample = Sample(
            U_sample=carry_state.U,
            log_L_constraint=log_L_constraint,
            log_L=carry_state.log_L,
            num_likelihood_evaluations=carry_state.num_likelihood_evals
        )
        phantom_samples = jax.tree.map(lambda x: jnp.zeros((0,) + x.shape, x.dtype), sample)
        return sample, phantom_samples
