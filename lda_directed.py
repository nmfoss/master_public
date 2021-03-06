# Modified from; https://stackoverflow.com/questions/45170093/latent-dirichlet-allocation-with-prior-topic-words

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.utils import check_random_state
from sklearn.decomposition._online_lda import _dirichlet_expectation_2d
import numpy as np

class DirectedLDA(LatentDirichletAllocation):
    
    def __init__(self, 
        n_components=10,
        doc_topic_prior=None,
        topic_word_prior=None,
        learning_method='batch',
        learning_decay=0.7,
        learning_offset=10.0,
        max_iter=10,
        batch_size=128,
        evaluate_every=-1,
        total_samples=1000000.0,
        perp_tol=0.1,
        mean_change_tol=0.001,
        max_doc_update_iter=100,
        n_jobs=None,
        verbose=0,
        random_state=None,
        ptws=None):
        

        super(DirectedLDA, self).__init__(
            n_components,
            doc_topic_prior,
            topic_word_prior,
            learning_method,
            learning_decay,
            learning_offset,
            max_iter,
            batch_size,
            evaluate_every,
            total_samples,
            perp_tol,
            mean_change_tol,
            max_doc_update_iter,
            n_jobs,
            verbose,
            random_state)
        self.ptws = ptws

        
    def _init_latent_vars(self, n_features):
        
        self.random_state_ = check_random_state(self.random_state)
        self.n_batch_iter_ = 1
        self.n_iter_ = 0
        
        if self.doc_topic_prior is None:
            self.doc_topic_prior_ = 1. / self.n_components
        else:
            self.doc_topic_prior_ = self_doc_topic_prior
            
        if self.topic_word_prior is None:
            self.topic_word_prior_ = 1. / self.n_components
        else:
            self.topic_word_prior_ = self.topic_word_prior
        
        init_gamma = 100.
        init_var = 1. / init_gamma
        self.components_ = self.random_state_.gamma(init_gamma, init_var, (self.n_components, n_features))

        
        if self.ptws is not None:
            
            for index in range(self.n_components):
                self.components_[index] = self.ptws[index][1]

            '''
            for ptw in self.ptws:
                
                word_index = ptw[0]
                word_topic_values = ptw[1]
                
                print(self.components_)
                print(word_topic_values)
                
                self.components_[:, word_index] *= word_topic_values
            '''
        
        self.exp_dirichlet_component_ = np.exp(_dirichlet_expectation_2d(self.components_))