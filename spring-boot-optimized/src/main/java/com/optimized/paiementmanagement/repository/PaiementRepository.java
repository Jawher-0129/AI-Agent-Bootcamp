package com.optimized.paiementmanagement.repository;

import com.optimized.paiementmanagement.model.Paiement;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * Payment Repository - Optimized with:
 * - Custom queries for complex business logic
 * - Proper indexing utilization
 */
@Repository
public interface PaiementRepository extends JpaRepository<Paiement, Long> {
    
    List<Paiement> findByReservationId(Long reservationId);
    
    List<Paiement> findByStatus(Paiement.PaiementStatus status);
    
    Optional<Paiement> findByTransactionId(String transactionId);
    
    @Query("SELECT p FROM Paiement p WHERE p.datePaiement BETWEEN :startDate AND :endDate")
    List<Paiement> findByDateRange(@Param("startDate") LocalDateTime startDate, 
                                    @Param("endDate") LocalDateTime endDate);
    
    @Query("SELECT p FROM Paiement p WHERE p.reservationId = :reservationId AND p.status = :status")
    List<Paiement> findByReservationIdAndStatus(@Param("reservationId") Long reservationId, 
                                                  @Param("status") Paiement.PaiementStatus status);
}
